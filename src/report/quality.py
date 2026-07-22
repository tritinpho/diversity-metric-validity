"""Phase-1 data-quality report: counts, missingness, length, duplication.

Output is intentionally descriptive and neutral (supply-side measurement). It
documents the *shape and completeness* of the snapshot — not any substantive
claim about coverage — so the corpus can be assessed before metrics are built.
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")  # headless backend; must precede pyplot import
import matplotlib.pyplot as plt
import pandas as pd

from src.config import Window, resolve_path
from src.dedupe.hashing import exact_duplicate_stats

_LOG = logging.getLogger("vnnews.report")
logging.getLogger("matplotlib").setLevel(logging.WARNING)  # quiet font/category INFO


# --------------------------------------------------------------------- helpers
def _md_table(df: pd.DataFrame, index: bool = False) -> str:
    """Render a DataFrame as a GitHub-flavored markdown table (no tabulate dep)."""
    cols = ([df.index.name or ""] if index else []) + [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |",
             "| " + " | ".join("---" for _ in cols) + " |"]
    for idx, row in df.iterrows():
        cells = ([str(idx)] if index else []) + [
            "" if pd.isna(v) else (f"{v:.1f}" if isinstance(v, float) else str(v))
            for v in row
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _pub_date(series: pd.Series, tz: str = "Asia/Ho_Chi_Minh") -> pd.Series:
    """Extract the publish date, in project tz, from ISO publish_datetime strings.

    ``format="ISO8601"`` is not optional: the corpus mixes second- and
    microsecond-precision stamps, and without it pandas infers a single format
    from the first row and silently coerces the rest to NaT (994 rows, all one
    outlet's sitemap-discovered articles, vanished from the per-day counts).

    The date is taken in the project timezone, not UTC — an article published
    06:00 +07:00 belongs to that day, not the one before.
    """
    return (pd.to_datetime(series, format="ISO8601", errors="coerce", utc=True)
              .dt.tz_convert(tz).dt.date)


# ------------------------------------------------------------------- plotting
def _bar(figpath: Path, labels, values, title: str, ylabel: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([str(x) for x in labels], values, color="#3b76a8")
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(figpath, dpi=110)
    plt.close(fig)


def _coverage_heatmap(df: pd.DataFrame, figpath: Path, tz: str) -> None:
    """Outlet x publish-day article counts — makes the collection gaps visible."""
    w = df.assign(_d=_pub_date(df["publish_datetime"], tz)).dropna(subset=["_d"])
    mat = w.pivot_table(index="outlet", columns="_d", values="article_id",
                        aggfunc="count", fill_value=0)
    mat = mat.loc[mat.sum(axis=1).sort_values(ascending=False).index]
    fig, ax = plt.subplots(figsize=(max(7, 0.32 * mat.shape[1]), 0.38 * len(mat) + 1.6))
    # Clip the scale at the 98th percentile: a single outlier day would
    # otherwise absorb most of the colour range and flatten the contrast that
    # makes the gaps legible.
    vmax = float(pd.Series(mat.to_numpy().ravel()).quantile(0.98)) or None
    im = ax.imshow(mat.to_numpy(), aspect="auto", cmap="viridis",
                   interpolation="nearest", vmin=0, vmax=vmax)
    ax.set_yticks(range(len(mat)), mat.index, fontsize=8)
    step = max(1, mat.shape[1] // 15)
    ax.set_xticks(range(0, mat.shape[1], step),
                  [str(c)[5:] for c in mat.columns[::step]], rotation=90, fontsize=7)
    ax.set_title("Articles per outlet x publish day (dark = no collection)")
    fig.colorbar(im, ax=ax, label="articles")
    fig.tight_layout()
    fig.savefig(figpath, dpi=110)
    plt.close(fig)


def _make_plots(df: pd.DataFrame, figures_dir: Path,
                tz: str = "Asia/Ho_Chi_Minh") -> dict[str, Path]:
    figs: dict[str, Path] = {}

    p = figures_dir / "coverage_heatmap.png"
    _coverage_heatmap(df, p, tz)
    figs["coverage"] = p

    per_outlet = df.groupby("outlet").size().sort_values(ascending=False)
    p = figures_dir / "articles_per_outlet.png"
    _bar(p, per_outlet.index, per_outlet.to_numpy(), "Articles per outlet", "articles")
    figs["per_outlet"] = p

    wc = df.groupby("outlet")["word_count"].mean().sort_values(ascending=False)
    p = figures_dir / "mean_length_per_outlet.png"
    _bar(p, wc.index, wc.to_numpy(), "Mean length per outlet (VN word tokens)", "tokens")
    figs["mean_len"] = p

    by_day = df.assign(d=_pub_date(df["publish_datetime"], tz)).dropna(subset=["d"])
    if not by_day.empty:
        counts = by_day.groupby("d").size().sort_index()
        p = figures_dir / "articles_per_day.png"
        _bar(p, counts.index, counts.to_numpy(), "Articles per publish day", "articles")
        figs["per_day"] = p

    sec = df.dropna(subset=["section"]).groupby("section").size().sort_values(
        ascending=False).head(12)
    if not sec.empty:
        p = figures_dir / "articles_per_section.png"
        _bar(p, sec.index, sec.to_numpy(), "Articles per section (top 12)", "articles")
        figs["per_section"] = p

    return figs


# --------------------------------------------------------------------- tables
def _counts_per_outlet(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["outlet", "outlet_type"]).size().reset_index(name="articles")
    return g.sort_values("articles", ascending=False)


def _missingness(df: pd.DataFrame) -> pd.DataFrame:
    fields = ["body", "section", "publish_datetime", "author"]
    rows = []
    for outlet, sub in df.groupby("outlet"):
        row = {"outlet": outlet, "n": len(sub)}
        for f in fields:
            row[f"%miss_{f}"] = round(100 * sub[f].isna().mean(), 1)
        rows.append(row)
    overall = {"outlet": "ALL", "n": len(df)}
    for f in fields:
        overall[f"%miss_{f}"] = round(100 * df[f].isna().mean(), 1)
    return pd.DataFrame(rows + [overall])


def _length_per_outlet(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("outlet")["word_count"].agg(["count", "mean", "median"]).reset_index()
    g["mean"] = g["mean"].round(1)
    g["median"] = g["median"].round(1)
    return g.rename(columns={"count": "n_with_body"})


def _section_table(df: pd.DataFrame) -> pd.DataFrame:
    g = (df.assign(section=df["section"].fillna("(none)"))
           .groupby(["outlet", "section"]).size().reset_index(name="articles"))
    return g.sort_values(["outlet", "articles"], ascending=[True, False])


def _syndication(df: pd.DataFrame) -> dict[str, int]:
    """Clusters of verbatim-identical bodies that span more than one outlet."""
    bodied = df[df["dedupe_cluster_id"].notna()]
    if bodied.empty:
        return {"cross_outlet_clusters": 0, "articles_in_cross_outlet_clusters": 0}
    per_cluster_outlets = bodied.groupby("dedupe_cluster_id")["outlet"].nunique()
    cross = per_cluster_outlets[per_cluster_outlets > 1].index
    involved = int(bodied["dedupe_cluster_id"].isin(cross).sum())
    return {"cross_outlet_clusters": int(len(cross)),
            "articles_in_cross_outlet_clusters": involved}


def _near_dup_summary(df: pd.DataFrame) -> dict[str, float] | None:
    """Near-duplicate (same-story) stats, if the near-dup pass has been run.

    The rate is taken over every body-bearing row, *not* over the rows carrying
    a cluster id. Those denominators diverge whenever the pass is stale — it is
    a separate on-demand step, so a corpus that has grown since the last run
    leaves most rows unlabelled. Dividing by the labelled subset turned 52
    copies over 1,423 labelled rows into a published "3.7% near-duplicate rate"
    for a 48,310-row corpus. ``stale`` flags that state so the report can say so
    rather than quietly report a rate for 3% of the data.
    """
    if "near_dup_cluster_id" not in df.columns or df["near_dup_cluster_id"].isna().all():
        return None
    labelled = df[df["near_dup_cluster_id"].notna()]
    bodied = int(df["body"].notna().sum())
    sizes = labelled.groupby("near_dup_cluster_id").size()
    nout = labelled.groupby("near_dup_cluster_id")["outlet"].nunique()
    cross = nout[nout > 1].index
    copies = int(df.get("is_near_duplicate", pd.Series(dtype=bool)).sum())
    return {
        "clusters_multi": int((sizes > 1).sum()),
        "copies": copies,
        "labelled": int(len(labelled)),
        "bodied": bodied,
        "stale": bool(len(labelled) < bodied),
        "rate": (copies / bodied) if bodied else 0.0,
        "largest_cluster": int(sizes.max()) if len(sizes) else 0,
        "cross_outlet_clusters": int(len(cross)),
        "articles_in_cross_outlet": int(labelled["near_dup_cluster_id"].isin(cross).sum()),
    }


def _coverage(df: pd.DataFrame, tz: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Per-outlet day coverage: which outlet-days the snapshot actually observed.

    Collection gaps here are not missing-at-random. Outlets served by a single
    short-retention feed lose a whole day whenever a scheduled run is missed,
    so day coverage varies systematically across outlets — and, because feed
    architecture correlates with outlet type, across ``outlet_type`` too. Any
    metric pooled over the corpus inherits that bias, which is why coverage is
    reported next to the raw counts rather than left implicit.
    """
    d = _pub_date(df["publish_datetime"], tz)
    w = df.assign(_d=d).dropna(subset=["_d"])
    days = sorted(w["_d"].unique())
    mat = w.pivot_table(index="outlet", columns="_d", values="article_id",
                        aggfunc="count", fill_value=0)
    mat = mat.reindex(columns=days, fill_value=0)

    med = mat.median(axis=1)
    zero = mat == 0
    thin = mat.lt(med * 0.25, axis=0) & (mat > 0)

    types = w.drop_duplicates("outlet").set_index("outlet")["outlet_type"]
    tbl = pd.DataFrame({
        "outlet": mat.index,
        "outlet_type": [types.get(o) for o in mat.index],
        "articles": mat.sum(axis=1).to_numpy(),
        "days_observed": (~zero).sum(axis=1).to_numpy(),
        "days_missing": zero.sum(axis=1).to_numpy(),
        "days_thin": thin.sum(axis=1).to_numpy(),
        "median_per_day": med.round(0).to_numpy(),
    }).sort_values("days_observed")

    # Edge days where the whole corpus is far below a normal day are ramp-up or
    # cut-off artefacts, not outlet-level gaps; without flagging them every
    # outlet looks like it "missed" days that were never collected at all.
    daily_total = mat.sum(axis=0)
    partial = [c for c in mat.columns if daily_total[c] < 0.25 * daily_total.median()]

    clean = [c for c in mat.columns if not zero[c].any() and not thin[c].any()]
    by_type = (tbl.groupby("outlet_type")["days_observed"].mean().round(1)
                  .reset_index().rename(columns={"days_observed": "mean_days_observed"}))
    stats = {
        "n_days": len(days), "n_outlets": len(mat.index),
        "cells": int(mat.size), "zero_cells": int(zero.to_numpy().sum()),
        "thin_cells": int(thin.to_numpy().sum()),
        "clean_days": len(clean), "by_type": by_type,
        "first_day": days[0], "last_day": days[-1],
        "partial_days": partial,
        # A final day cut off mid-collection looks normal by volume but covers
        # fewer publishing hours — invisible to the volume check above.
        "last_day_max_hour": int(
            pd.to_datetime(w.loc[w["_d"] == days[-1], "publish_datetime"],
                           format="ISO8601", utc=True)
              .dt.tz_convert(tz).dt.hour.max()),
    }
    return tbl, stats


# ---------------------------------------------------------------------- main
def generate_report(
    df: pd.DataFrame, cfg: dict[str, Any], window: Window, generated_at: datetime
) -> Path:
    figures_dir = resolve_path(cfg, "figures_dir")
    reports_dir = resolve_path(cfg, "reports_dir")
    figures_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    tz = cfg["project"]["timezone"]
    figs = _make_plots(df, figures_dir, tz)
    dup = exact_duplicate_stats(df)
    synd = _syndication(df)
    near = _near_dup_summary(df)
    cov_tbl, cov = _coverage(df, tz)
    lang_counts = df["lang"].value_counts(dropna=False)
    non_vi = int(df["lang"].notna().sum() - (df["lang"] == "vi").sum())
    seg_methods = df["seg_method"].dropna().value_counts().to_dict()

    def rel(p: Path) -> str:
        return p.relative_to(reports_dir).as_posix()

    parts: list[str] = []
    parts.append("# Vietnamese News Diversity — Phase 1 Data-Quality Report\n")
    parts.append(
        f"*Supply-side snapshot. Descriptive completeness check on the published "
        f"cross-section; no exposure or substantive-coverage claims.*\n")
    parts.append(
        f"- **Generated:** {generated_at.isoformat()}\n"
        f"- **Publish-date span (observed in the corpus):** {cov['first_day']} → "
        f"{cov['last_day']} ({tz}), {cov['n_days']} days\n"
        f"- **Configured collection window:** {window.start.date()} → "
        f"{window.end.date()}\n"
        f"- **Articles:** {len(df)}  |  **Outlets:** {df['outlet'].nunique()}  |  "
        f"**Sections observed:** {df['section'].nunique(dropna=True)}\n"
        f"- **Segmentation:** {seg_methods} (token counts)\n")
    parts.append(
        "\n_Every statistic below is computed over the **whole corpus**, not "
        "filtered to the configured window — the two differ, because the corpus "
        "accumulated across runs whose rolling window moved. The observed span "
        "is the authoritative one for reading this report; fixing the analysis "
        "window is a separate decision (see §4)._\n")

    parts.append("\n## 1. Articles per outlet\n")
    parts.append(_md_table(_counts_per_outlet(df)))
    if "per_outlet" in figs:
        parts.append(f"\n![Articles per outlet]({rel(figs['per_outlet'])})\n")

    parts.append("\n## 2. Articles per outlet × section\n")
    parts.append(
        "_Section provenance differs by outlet, which is itself a measurement-"
        "validity observation (not a data error). VnExpress and Tuổi Trẻ supply "
        "clean per-section RSS, so their `section` values are controlled slugs "
        "(`thoi-su`, `phap-luat`, …). Nhân Dân (party_official) exposes no reliable "
        "per-section feed and uses flat article URLs; its `section` is recovered "
        "from page categories where present — natural-language labels mixing topical "
        "and geographic taxonomies (`Thể thao`, `Môi trường`, `Duyên hải Nam Trung "
        "Bộ và Tây Nguyên`) — and `(none)` otherwise. The section vocabulary is "
        "therefore not directly comparable across outlet types and will need "
        "harmonisation before any section-based diversity metric._\n\n")
    parts.append(_md_table(_section_table(df)))
    if "per_section" in figs:
        parts.append(f"\n![Articles per section]({rel(figs['per_section'])})\n")

    parts.append("\n## 3. Articles per publish day\n")
    by_day = df.assign(d=_pub_date(df["publish_datetime"], tz)).dropna(subset=["d"])
    if not by_day.empty:
        day_tbl = by_day.groupby("d").size().reset_index(name="articles")
        parts.append(_md_table(day_tbl))
    if "per_day" in figs:
        parts.append(f"\n![Articles per day]({rel(figs['per_day'])})\n")

    parts.append("\n## 4. Coverage: which outlet-days were observed\n")
    pct_zero = 100 * cov["zero_cells"] / cov["cells"] if cov["cells"] else 0.0
    parts.append(
        f"- Outlet x day cells: **{cov['cells']}** "
        f"({cov['n_outlets']} outlets x {cov['n_days']} days)\n"
        f"- Cells with **no articles collected**: **{cov['zero_cells']}** "
        f"({pct_zero:.1f}%)\n"
        f"- Cells unusually thin (<25% of that outlet's median day): "
        f"**{cov['thin_cells']}**\n"
        f"- Days on which **every** outlet was collected at normal volume: "
        f"**{cov['clean_days']}** of {cov['n_days']}\n")
    if cov["partial_days"]:
        parts.append(
            f"- Corpus-wide **partial days** (total volume <25% of a normal day — "
            f"collection ramping up, rather than outlet-level gaps): "
            f"{', '.join(str(d) for d in cov['partial_days'])}\n")
    if cov["last_day_max_hour"] < 21:
        parts.append(
            f"- The final day, **{cov['last_day']}**, is **truncated**: the "
            f"latest article published on it is from hour "
            f"{cov['last_day_max_hour']:02d}:00, so it covers only part of a "
            f"publishing day. Its volume looks normal, so this does not show up "
            f"as a thin day — but it is not a complete day of supply.\n")
    if cov["partial_days"] or cov["last_day_max_hour"] < 21:
        parts.append(
            "\n_Those edge days inflate `days_missing` for every outlet in the "
            "table below, since no outlet was being collected on them. They are "
            "why the observed span is wider than the analysis window, and they "
            "fall outside it._\n")

    acfg = cfg.get("analysis") or {}
    if acfg.get("start") and acfg.get("end"):
        a_lo = pd.Timestamp(str(acfg["start"]), tz=tz)
        a_hi = pd.Timestamp(str(acfg["end"]), tz=tz) + pd.Timedelta(days=1)
        dts = (pd.to_datetime(df["publish_datetime"], format="ISO8601",
                              errors="coerce", utc=True).dt.tz_convert(tz))
        adf = df[(dts >= a_lo) & (dts < a_hi)]
        _, acov = _coverage(adf, tz)
        flagged = ", ".join(str(d) for d in acfg.get("flag_days") or []) or "none"
        parts.append(
            f"\n### Analysis window\n\n"
            f"`config.yaml: analysis` — **{acfg['start']} → {acfg['end']}**, "
            f"{acov['n_days']} days ({acov['n_days'] // 7} calendar weeks), "
            f"**{len(adf)}** articles. Metrics are computed on this subset; the "
            f"corpus as released keeps the full span above.\n\n"
            f"- Outlet-days with no articles: **{acov['zero_cells']}** of "
            f"{acov['cells']} ({100 * acov['zero_cells'] / acov['cells']:.1f}%)\n"
            f"- Fully-observed days (balanced-panel subset): "
            f"**{acov['clean_days']}** of {acov['n_days']}\n"
            f"- Days retained but flagged for robustness checks: {flagged}\n")
        parts.append(
            "\n_The window is a whole number of calendar weeks so that "
            "day-of-week is balanced — weekend supply is lighter and skews away "
            "from politics, which would otherwise bias topic composition. The "
            "truncated final collection day is excluded. Note that the zero-cell "
            "rate is essentially identical across every candidate window, so the "
            "window choice does not mitigate the coverage confound; only the "
            "panel treatment does._\n")
    parts.append(
        "\n_These gaps are **not** missing-at-random and are a property of the "
        "collection, not of publishing. Outlets served by a single "
        "short-retention feed lose a whole day whenever a scheduled run is "
        "missed, while outlets with per-section feeds or deep sitemaps can be "
        "backfilled. Because feed architecture correlates with structural type, "
        "day coverage varies systematically across `outlet_type` — so an "
        "outlet's share of the pooled corpus reflects collection availability as "
        "well as publishing volume. Metrics should therefore be computed on an "
        "**unbalanced outlet-day panel** (per day, then aggregated over observed "
        "outlet-days) rather than pooled over the corpus, with the fully-observed "
        "days above available as a balanced-panel robustness check._\n")
    parts.append("\n" + _md_table(cov_tbl))
    parts.append("\n**Mean days observed by outlet type**\n\n")
    parts.append(_md_table(cov["by_type"]))
    if "coverage" in figs:
        parts.append(f"\n![Coverage heatmap]({rel(figs['coverage'])})\n")

    parts.append("\n## 5. Missingness by field (% null)\n")
    parts.append(_md_table(_missingness(df)))

    parts.append("\n## 6. Article length (Vietnamese word tokens)\n")
    parts.append(_md_table(_length_per_outlet(df)))
    if "mean_len" in figs:
        parts.append(f"\n![Mean length per outlet]({rel(figs['mean_len'])})\n")

    parts.append("\n## 7. Language\n")
    lang_tbl = lang_counts.reset_index()
    lang_tbl.columns = ["lang", "articles"]
    parts.append(_md_table(lang_tbl))
    parts.append(f"\n_Non-`vi` (flagged): {non_vi}._\n")

    parts.append("\n## 8. Duplication\n")
    parts.append(
        f"- Articles with extractable body: **{dup['articles_with_body']}**\n"
        f"- Exact-duplicate copies (verbatim body, after first): "
        f"**{dup['exact_duplicate_copies']}**\n"
        f"- Exact-duplicate rate: **{100 * dup['exact_duplicate_rate']:.1f}%**\n"
        f"- Distinct content clusters: **{dup['unique_content_clusters']}**\n"
        f"- Cross-outlet verbatim clusters (syndication signal): "
        f"**{synd['cross_outlet_clusters']}** "
        f"({synd['articles_in_cross_outlet_clusters']} articles)\n")
    if near is None:
        parts.append("- Near-duplicate (same-story) clustering: _not yet run "
                     "(`python -m src.dedupe.near_dup`)._\n")
    else:
        dd = cfg.get("dedupe", {})
        parts.append(
            f"- Near-duplicate (same-story) copies: **{near['copies']}** "
            f"({100 * near['rate']:.1f}% of {near['bodied']} body-bearing articles), "
            f"in **{near['clusters_multi']}** multi-article clusters "
            f"(largest: {near['largest_cluster']})\n"
            f"- **Cross-outlet** same-story clusters: **{near['cross_outlet_clusters']}** "
            f"({near['articles_in_cross_outlet']} articles) — the syndication/overlap "
            f"signal that exact-hash misses\n"
            f"- Clustering parameters: cosine >= {dd.get('near_dup_threshold')}, "
            f"linkage restricted to articles published within "
            f"{dd.get('near_dup_max_hours')}h of each other\n")
        parts.append(
            "\n_The temporal restriction is load-bearing, not a detail. Under an "
            "unrestricted threshold, recurring templated genres — daily gold- and "
            "petrol-price columns, fixture lists — chain across days into single "
            "clusters (the largest reached 189 articles spanning 14 outlets and "
            "the full month), because each edition is near-identical to the next "
            "day's. Restricting linkage to a window shorter than that recurrence "
            "period separates same-story republication from same-template "
            "recurrence; it moves the cross-outlet article count by roughly a "
            "fifth, so the parameter belongs in any reported figure._\n")
        if near["stale"]:
            parts.append(
                f"\n> **⚠ These near-duplicate figures are stale.** Only "
                f"{near['labelled']} of {near['bodied']} body-bearing articles "
                f"carry a cluster id, so the pass has not been re-run since the "
                f"corpus grew. Re-run `python -m src.dedupe.near_dup` before "
                f"citing anything in this section.\n")

    md = "\n".join(parts) + "\n"
    out = reports_dir / "quality_report.md"
    out.write_text(md, encoding="utf-8")
    _LOG.info("wrote data-quality report -> %s", out)
    return out
