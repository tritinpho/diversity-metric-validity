"""Threshold calibration for near-duplicate detection (Phase 2 validity work).

``dedupe.near_dup_threshold`` is currently justified by a comment in
``config.yaml``. That is not defensible in a measurement-validity paper: the
threshold sets how much cross-outlet overlap the corpus appears to contain, so
it needs an empirical precision/recall curve behind it, not an assertion.

This module builds that evidence in two steps::

    python -m src.dedupe.calibrate sample        # draw pairs, write labelling sheet
    # ...a human labels reports/calibration/pairs_sample.csv...
    python -m src.dedupe.calibrate score         # precision / recall by threshold

**Why stratified.** Within the analysis window there are ~40.7M candidate pairs
inside the 12h linkage window, of which only ~105k reach cosine 0.70 and ~2k
reach 0.94. True same-story pairs are far rarer still, so a uniform random
sample would return essentially no positives and support no recall estimate.
Instead pairs are binned by similarity, sampled within band, and each band is
re-weighted by its known population size when the rates are computed. Bands are
narrow around the decision boundary, where the threshold actually gets decided,
and coarse in the tail.

**What recall means here.** Recall is measured against the >=0.70 candidate pool,
not against all pairs. A same-story pair rewritten so heavily that it falls
below 0.70 is invisible to this design; the tail bands are sampled partly to
show whether that population looks non-empty. Report the figure as
"recall within the >=0.70 candidate pool" and not as unqualified recall.

The labelling sheet deliberately **hides the similarity score** — showing it
would anchor the labeller on the model's own answer — and interleaves bands in a
fixed-seed shuffle so labelling drift is not confounded with similarity.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.config import load_config, resolve_path, setup_logging
from src.dedupe.near_dup import embed_with_cache

_LOG = logging.getLogger("vnnews.calibrate")

# Round 1 (low, high, n_to_sample). Dense near the boundary, sparse in the tail.
BANDS_R1: list[tuple[float, float, int]] = [
    (0.70, 0.75, 8),
    (0.75, 0.80, 8),
    (0.80, 0.85, 12),
    (0.85, 0.88, 20),
    (0.88, 0.90, 25),
    (0.90, 0.92, 25),
    (0.92, 0.94, 30),   # just below threshold — decides whether 0.94 is too strict
    (0.94, 0.96, 30),
    (0.96, 0.98, 25),
    (0.98, 1.01, 25),
]

# Round 2 corrects two design errors that the round-1 labels exposed.
#
# (1) The 0.70 floor was too high. Confirmed same-story pairs turned up at
#     0.7157 and 0.7490 — right at the edge — so real positives certainly sit
#     below the old pool and were invisible to the estimate entirely.
# (2) The low bands were drastically under-sampled: [0.70,0.85) holds 85% of
#     the old pool but received 28 of 208 labels (0.03%, against 3.95% in the
#     top three bands). Recall at 0.94 came out 0.060 with a plausible range of
#     0.024-0.144 — i.e. not identified.
#
# Allocation leans toward the decision-relevant region (0.65-0.85) while still
# probing the three new bands hard enough to tell whether their rate is
# negligible or material. The high bands are untouched: precision up there is
# already well estimated and more labels would buy little.
BANDS_R2: list[tuple[float, float, int]] = [
    (0.55, 0.60, 15),
    (0.60, 0.65, 15),
    (0.65, 0.70, 18),
    (0.70, 0.75, 18),
    (0.75, 0.80, 14),
    (0.80, 0.85, 12),
]

ROUNDS = {1: BANDS_R1, 2: BANDS_R2}
FLOOR = 0.70          # round-1 floor, retained for the recall caveat wording
SEED = 20260722
PREVIEW_CHARS = 420


# ------------------------------------------------------------------ candidates
def _analysis_subset(df: pd.DataFrame, cfg: dict[str, Any]) -> pd.DataFrame:
    """Body-bearing rows inside the configured analysis window."""
    tz = cfg["project"]["timezone"]
    a = cfg.get("analysis") or {}
    out = df[df["body"].notna()]
    if a.get("start") and a.get("end"):
        dts = (pd.to_datetime(out["publish_datetime"], format="ISO8601",
                              errors="coerce", utc=True).dt.tz_convert(tz))
        lo = pd.Timestamp(str(a["start"]), tz=tz)
        hi = pd.Timestamp(str(a["end"]), tz=tz) + pd.Timedelta(days=1)
        out = out[(dts >= lo) & (dts < hi)]
    return out.reset_index(drop=True)


def candidate_pairs(
    emb: np.ndarray, secs: np.ndarray, max_hours: float, floor: float = FLOOR,
    block: int = 2000,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """All (i, j, sim) with sim >= floor and |t_i - t_j| <= max_hours.

    Rows must already be sorted by ``secs`` ascending. Mirrors the blocking and
    windowing in ``near_dup.cluster_near_dups`` so the sampled pool is exactly
    the population the clusterer draws its links from.
    """
    n = len(emb)
    hi = np.searchsorted(secs, secs + int(max_hours * 3600), side="right")
    I: list[np.ndarray] = []
    J: list[np.ndarray] = []
    S: list[np.ndarray] = []
    total = 0
    for s in range(0, n - 1, block):
        e = min(s + block, n)
        hm = int(hi[e - 1])
        if hm <= s + 1:
            continue
        sim = emb[s:e] @ emb[s:hm].T
        cols = np.arange(s, hm)[None, :]
        rows = np.arange(s, e)[:, None]
        valid = (cols > rows) & (cols < hi[s:e][:, None])
        total += int(valid.sum())
        keep = valid & (sim >= floor)
        bi, bj = np.nonzero(keep)
        if len(bi):
            I.append(bi + s)
            J.append(bj + s)
            S.append(sim[bi, bj])
    _LOG.info("candidate pairs within %gh: %d total, %d at cosine>=%.2f",
              max_hours, total, sum(len(x) for x in I), floor)
    if not I:
        return np.array([], "int64"), np.array([], "int64"), np.array([], "float32")
    return np.concatenate(I), np.concatenate(J), np.concatenate(S)


# --------------------------------------------------------------------- sampling
def draw(sub: pd.DataFrame, I, J, S, bands: list[tuple[float, float, int]],
         seed: int = SEED, exclude: set[frozenset] | None = None,
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    """Stratified sample plus the per-band population sizes used to re-weight it.

    ``exclude`` holds ``frozenset({url_a, url_b})`` for pairs already drawn in an
    earlier round. Those are removed from the candidate pool *before* sampling
    but still counted in the band population, so the later round samples the
    remainder while the weights continue to describe the whole band. With
    sampling fractions well under 1% the two rounds can then be pooled and
    treated as one simple random sample per band.
    """
    rng = np.random.default_rng(seed)
    exclude = exclude or set()
    urls = sub["url"].to_numpy()
    rows, strata = [], []
    for lo, hi, k in bands:
        idx = np.flatnonzero((S >= lo) & (S < hi))
        population = int(len(idx))
        if exclude:
            idx = np.array([p for p in idx
                            if frozenset((urls[I[p]], urls[J[p]])) not in exclude],
                           dtype="int64")
        take = min(k, len(idx))
        pick = rng.choice(idx, size=take, replace=False) if take else np.array([], "int64")
        strata.append({"band_lo": lo, "band_hi": hi,
                       "population": population, "sampled": int(take)})
        for p in pick:
            a, b = int(I[p]), int(J[p])
            ra, rb = sub.iloc[a], sub.iloc[b]
            rows.append({
                "pair_id": f"{ra.article_id[:8]}_{rb.article_id[:8]}",
                "band_lo": lo, "band_hi": hi, "similarity": round(float(S[p]), 4),
                "cross_outlet": int(ra.outlet != rb.outlet),
                "outlet_a": ra.outlet, "published_a": str(ra.publish_datetime),
                "headline_a": ra.headline, "lead_a": (ra.body or "")[:PREVIEW_CHARS],
                "url_a": ra.url,
                "outlet_b": rb.outlet, "published_b": str(rb.publish_datetime),
                "headline_b": rb.headline, "lead_b": (rb.body or "")[:PREVIEW_CHARS],
                "url_b": rb.url,
                "label": "", "notes": "",
            })
    out = pd.DataFrame(rows)
    # Interleave bands so labelling fatigue is not confounded with similarity.
    out = out.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
    return out, strata


_HTML = """<!doctype html><meta charset="utf-8"><title>Near-dup labelling</title>
<style>
 body{font:15px/1.55 system-ui,sans-serif;max-width:1180px;margin:0 auto;padding:24px;background:#faf9f7;color:#1a1a1a}
 h1{font-size:19px;margin:0 0 4px} .sub{color:#666;font-size:13px;margin-bottom:18px}
 #bar{position:sticky;top:0;background:#faf9f7;padding:12px 0;border-bottom:1px solid #ddd;z-index:9}
 .pair{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:18px 0}
 .side{background:#fff;border:1px solid #e2e0dc;border-radius:8px;padding:14px}
 .meta{font-size:12px;color:#777;margin-bottom:6px}
 .hl{font-weight:600;margin-bottom:8px} .lead{font-size:14px;color:#333}
 .btns{display:flex;gap:8px;margin:10px 0 4px}
 button{font:inherit;padding:8px 18px;border-radius:6px;border:1px solid #ccc;background:#fff;cursor:pointer}
 button:hover{background:#f0efec}
 .y{border-color:#2d7a3e;color:#2d7a3e} .n{border-color:#a33;color:#a33}
 .done{opacity:.45} .cur{outline:2px solid #3b76a8;outline-offset:6px;border-radius:10px}
 #dl{background:#1a1a1a;color:#fff;border-color:#1a1a1a}
 kbd{background:#eee;border:1px solid #ccc;border-radius:3px;padding:1px 5px;font-size:12px}
</style>
<h1>Near-duplicate labelling</h1>
<div class="sub">Same <b>story</b> = the two articles report the same specific event/announcement.
Not the same story = same topic, recurring column, or a later development with new facts.
Similarity scores are hidden on purpose. <kbd>y</kbd> same &middot; <kbd>n</kbd> different &middot; <kbd>s</kbd> skip &middot; <kbd>u</kbd> undo</div>
<div id="bar"><span id="prog"></span> &nbsp; <button id="dl">Download labels CSV</button>
 <span id="saved" style="color:#2d7a3e;font-size:12px"></span></div>
<div id="list"></div>
<script>
const D=__DATA__, KEY='near-dup-labels__SUFFIX__'; let cur=0;
const L=document.getElementById('list'), P=document.getElementById('prog');
// Labels live only in this page until downloaded, so mirror them to
// localStorage on every keystroke — a refresh or accidental close would
// otherwise discard the whole session's work.
try{const s=JSON.parse(localStorage.getItem(KEY)||'{}');
    D.forEach(d=>{if(s[d.pair_id]!==undefined)d.label=s[d.pair_id]})}catch(e){}
function save(){try{const s={};D.forEach(d=>{if(d.label!==undefined)s[d.pair_id]=d.label});
 localStorage.setItem(KEY,JSON.stringify(s));
 document.getElementById('saved').textContent='saved locally'}catch(e){}}
D.forEach((d,i)=>{
 const el=document.createElement('div'); el.id='p'+i;
 el.innerHTML=`<div class="btns"><b>${i+1}.</b>
   <button class="y" onclick="mark(${i},1)">Same story</button>
   <button class="n" onclick="mark(${i},0)">Different</button>
   <button onclick="mark(${i},'')">Skip</button>
   <span id="s${i}" style="color:#666"></span></div>
  <div class="pair">
   <div class="side"><div class="meta">${d.outlet_a} &middot; ${d.published_a}
     &middot; <a href="${esc(d.url_a)}" target="_blank" rel="noopener">open source ↗</a></div>
     <div class="hl">${esc(d.headline_a)}</div><div class="lead">${esc(d.lead_a)}…</div></div>
   <div class="side"><div class="meta">${d.outlet_b} &middot; ${d.published_b}
     &middot; <a href="${esc(d.url_b)}" target="_blank" rel="noopener">open source ↗</a></div>
     <div class="hl">${esc(d.headline_b)}</div><div class="lead">${esc(d.lead_b)}…</div></div>
  </div>`;
 L.appendChild(el);
 if(d.label!==undefined)paint(i);
});
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML}
function paint(i){const v=D[i].label;
 document.getElementById('s'+i).textContent=v===1?'✓ same':(v===0?'✗ different':'skipped');
 document.getElementById('p'+i).classList.add('done')}
function mark(i,v){D[i].label=v;paint(i);save();
 if(i===cur)focus(Math.min(cur+1,D.length-1));upd()}
function focus(i){document.getElementById('p'+cur)?.classList.remove('cur');cur=i;
 const el=document.getElementById('p'+i);el.classList.add('cur');el.scrollIntoView({block:'center',behavior:'smooth'});upd()}
function upd(){const n=D.filter(d=>d.label!==''&&d.label!==undefined).length;P.textContent=`${n} / ${D.length} labelled — on #${cur+1}`}
addEventListener('keydown',e=>{if(e.target.tagName==='A')return;
 if(e.key==='y')mark(cur,1);else if(e.key==='n')mark(cur,0);
 else if(e.key==='s')mark(cur,'');else if(e.key==='u')focus(Math.max(0,cur-1));});
addEventListener('beforeunload',e=>{const n=D.filter(d=>d.label!==''&&d.label!==undefined).length;
 if(n>0&&!window.__dl){e.preventDefault();e.returnValue=''}});
document.getElementById('dl').onclick=()=>{window.__dl=1;
 const cols=['pair_id','similarity','band_lo','band_hi','cross_outlet','label'];
 const rows=[cols.join(',')].concat(D.map(d=>cols.map(c=>{
   const v=d[c]===undefined?'':d[c];return /[",\\n]/.test(''+v)?'"'+(''+v).replace(/"/g,'""')+'"':v}).join(',')));
 const b=new Blob([rows.join('\\n')],{type:'text/csv;charset=utf-8'});
 const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='pairs_labelled__SUFFIX__.csv';a.click()};
focus(0);upd();
</script>
"""


def write_sheets(sample: pd.DataFrame, strata: list[dict], outdir: Path,
                 suffix: str = "") -> tuple[Path, Path, Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    csv_p = outdir / f"pairs_sample{suffix}.csv"
    sample.to_csv(csv_p, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)

    keep = ["pair_id", "similarity", "band_lo", "band_hi", "cross_outlet",
            "outlet_a", "published_a", "headline_a", "lead_a", "url_a",
            "outlet_b", "published_b", "headline_b", "lead_b", "url_b"]
    # No initial ``label`` key: undefined means untouched, "" means deliberately
    # skipped, 0/1 means judged. Seeding it with "" would make every pair look
    # pre-skipped on load and defeat the restore-from-storage check.
    payload = sample[keep].to_dict("records")
    html_p = outdir / f"label{suffix}.html"
    html_p.write_text(_HTML.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
                           .replace("__SUFFIX__", suffix),
                      encoding="utf-8")

    strata_p = outdir / f"strata{suffix}.json"
    strata_p.write_text(json.dumps(strata, indent=2), encoding="utf-8")
    return csv_p, html_p, strata_p


# ---------------------------------------------------------------------- scoring
def score(labels: pd.DataFrame, strata: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Stratum-weighted precision / recall / F1 at each band edge.

    Each band's labelled positive rate is extrapolated to its full population,
    so the estimates describe the whole >=0.70 candidate pool rather than the
    sample. Thresholds are evaluated only at band edges — interpolating inside a
    band would assume a within-band distribution the sample cannot support.

    A band with no labels contributes zero estimated positives, which would
    quietly inflate precision and distort recall, so partial labelling raises
    rather than silently producing a plausible-looking curve.
    """
    lab = labels[labels["label"].isin([0, 1, "0", "1"])].copy()
    lab["label"] = lab["label"].astype(int)
    pop = {(s["band_lo"], s["band_hi"]): s["population"] for s in strata}

    est = []
    for (lo, hi), N in sorted(pop.items()):
        sl = lab[(lab["band_lo"] == lo) & (lab["band_hi"] == hi)]
        n, k = len(sl), int(sl["label"].sum())
        rate = (k / n) if n else float("nan")
        est.append({"lo": lo, "hi": hi, "N": N, "n": n, "k": k,
                    "rate": rate, "P": (N * rate) if n else 0.0})
    e = pd.DataFrame(est)

    empty = e[e["n"] == 0]
    if len(empty):
        raise SystemExit(
            "cannot score: no labels in band(s) "
            + ", ".join(f"[{r.lo:.2f},{r.hi:.2f})" for r in empty.itertuples())
            + ". An unlabelled band would be counted as containing zero true "
              "pairs, inflating precision and understating the true-pair total. "
              "Label at least a few pairs in every band, or drop those bands "
              "from strata.json deliberately.")
    thin = e[(e["n"] > 0) & (e["n"] < 5)]
    if len(thin):
        _LOG.warning("bands with <5 labels — rates there are very noisy: %s",
                     ", ".join(f"[{r.lo:.2f},{r.hi:.2f}) n={r.n}"
                               for r in thin.itertuples()))
    _LOG.info("scoring on %d labelled pairs of %d sampled", len(lab), len(labels))
    total_pos = e["P"].sum()

    rows = []
    for lo in sorted(e["lo"]):
        sel = e[e["lo"] >= lo]
        retrieved, tp = sel["N"].sum(), sel["P"].sum()
        prec = tp / retrieved if retrieved else float("nan")
        rec = tp / total_pos if total_pos else float("nan")
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else float("nan")
        rows.append({"threshold": lo, "pairs_retrieved": int(retrieved),
                     "est_true_pairs": round(tp, 1), "precision": round(prec, 3),
                     "recall_in_pool": round(rec, 3), "f1": round(f1, 3)})
    return pd.DataFrame(rows), e


# ------------------------------------------------------------------------- main
def _merge_strata(outdir: Path) -> list[dict[str, Any]]:
    """Union the per-round strata files: population is fixed, sampled counts add."""
    merged: dict[tuple[float, float], dict[str, Any]] = {}
    for p in sorted(outdir.glob("strata*.json")):
        for s in json.loads(p.read_text(encoding="utf-8")):
            key = (s["band_lo"], s["band_hi"])
            if key in merged:
                if merged[key]["population"] != s["population"]:
                    raise SystemExit(
                        f"band {key} has conflicting populations across rounds "
                        f"({merged[key]['population']} vs {s['population']}) — the "
                        f"corpus or embedding changed between draws, so the rounds "
                        f"cannot be pooled.")
                merged[key]["sampled"] += s["sampled"]
            else:
                merged[key] = dict(s)
    return [merged[k] for k in sorted(merged)]


def main() -> None:
    ap = argparse.ArgumentParser(description="Near-dup threshold calibration")
    sp = ap.add_subparsers(dest="cmd", required=True)
    sm = sp.add_parser("sample", help="draw a stratified pair sample and write labelling sheets")
    sm.add_argument("--round", type=int, default=1, choices=sorted(ROUNDS),
                    help="which band schedule to draw (later rounds exclude "
                         "pairs already drawn)")
    sp.add_parser("score", help="score every labelled round found on disk")
    args = ap.parse_args()

    cfg = load_config()
    setup_logging(cfg["logging"]["level"])
    outdir = resolve_path(cfg, "reports_dir") / "calibration"

    if args.cmd == "score":
        label_files = sorted(outdir.glob("pairs_labelled*.csv"))
        if not label_files:
            raise SystemExit(f"no labelled files in {outdir} — label a sheet first")
        labels = pd.concat([pd.read_csv(p) for p in label_files], ignore_index=True)
        labels = labels.drop_duplicates("pair_id")
        _LOG.info("pooling %d rounds: %s", len(label_files),
                  ", ".join(p.name for p in label_files))
        tbl, bands = score(labels, _merge_strata(outdir))
        print("\n=== per-band labelled positive rate ===")
        print(bands.to_string(index=False))
        print("\n=== precision / recall by threshold ===")
        print(tbl.to_string(index=False))
        floor = min(b["lo"] for _, b in bands.iterrows())
        print(f"\n(recall is within the >={floor:.2f} candidate pool, not absolute)")
        (outdir / "calibration_results.csv").write_text(
            tbl.to_csv(index=False), encoding="utf-8")
        _LOG.info("wrote %s", outdir / "calibration_results.csv")
        return

    bands = ROUNDS[args.round]
    suffix = "" if args.round == 1 else f"_r{args.round}"
    floor = min(lo for lo, _, _ in bands)
    exclude: set[frozenset] = set()
    for p in sorted(outdir.glob("pairs_sample*.csv")):
        prev = pd.read_csv(p)
        exclude |= {frozenset((a, b)) for a, b in zip(prev["url_a"], prev["url_b"])}
    if exclude:
        _LOG.info("excluding %d pairs already drawn in earlier rounds", len(exclude))

    dd = cfg["dedupe"]
    df = pd.read_parquet(resolve_path(cfg, "articles_parquet"))
    sub = _analysis_subset(df, cfg)
    _LOG.info("analysis-window body-bearing rows: %d", len(sub))

    body_chars = int(dd.get("embed_body_chars", 600))
    texts = [((h or "") + ". " + (b or "")[:body_chars]).strip()
             for h, b in zip(sub["headline"], sub["body"])]
    emb = embed_with_cache(sub["article_id"].tolist(), texts, dd["embedding_model"],
                           body_chars, resolve_path(cfg, "embeddings_cache"))

    secs = ((pd.to_datetime(sub["publish_datetime"], format="ISO8601", utc=True)
             - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta(seconds=1)).to_numpy()
    order = np.argsort(secs, kind="stable")
    sub, emb, secs = sub.iloc[order].reset_index(drop=True), emb[order], secs[order]

    I, J, S = candidate_pairs(emb, secs, float(dd.get("near_dup_max_hours") or 12),
                              floor=floor)
    sample, strata = draw(sub, I, J, S, bands, seed=SEED + args.round,
                          exclude=exclude)
    csv_p, html_p, strata_p = write_sheets(sample, strata, outdir, suffix)

    print(f"\n=== round {args.round} strata (population vs sampled) ===")
    print(pd.DataFrame(strata).to_string(index=False))
    print(f"\nsampled {len(sample)} new pairs "
          f"({int(sample['cross_outlet'].sum())} cross-outlet)")
    print(f"\n  label here : {html_p}")
    print(f"  or edit    : {csv_p}  (label column: 1 = same story, 0 = not)")
    print(f"  then run   : python -m src.dedupe.calibrate score   "
          f"(pools every round on disk)")


if __name__ == "__main__":
    main()
