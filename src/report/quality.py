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


def _pub_date(series: pd.Series) -> pd.Series:
    """Extract YYYY-MM-DD from ISO publish_datetime strings (NaT-safe)."""
    return pd.to_datetime(series, errors="coerce", utc=True).dt.date


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


def _make_plots(df: pd.DataFrame, figures_dir: Path) -> dict[str, Path]:
    figs: dict[str, Path] = {}

    per_outlet = df.groupby("outlet").size().sort_values(ascending=False)
    p = figures_dir / "articles_per_outlet.png"
    _bar(p, per_outlet.index, per_outlet.to_numpy(), "Articles per outlet", "articles")
    figs["per_outlet"] = p

    wc = df.groupby("outlet")["word_count"].mean().sort_values(ascending=False)
    p = figures_dir / "mean_length_per_outlet.png"
    _bar(p, wc.index, wc.to_numpy(), "Mean length per outlet (VN word tokens)", "tokens")
    figs["mean_len"] = p

    by_day = df.assign(d=_pub_date(df["publish_datetime"])).dropna(subset=["d"])
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
    """Near-duplicate (same-story) stats, if the near-dup pass has been run."""
    if "near_dup_cluster_id" not in df.columns or df["near_dup_cluster_id"].isna().all():
        return None
    bodied = df[df["near_dup_cluster_id"].notna()]
    sizes = bodied.groupby("near_dup_cluster_id").size()
    nout = bodied.groupby("near_dup_cluster_id")["outlet"].nunique()
    cross = nout[nout > 1].index
    copies = int(df.get("is_near_duplicate", pd.Series(dtype=bool)).sum())
    return {
        "clusters_multi": int((sizes > 1).sum()),
        "copies": copies,
        "rate": (copies / len(bodied)) if len(bodied) else 0.0,
        "cross_outlet_clusters": int(len(cross)),
        "articles_in_cross_outlet": int(bodied["near_dup_cluster_id"].isin(cross).sum()),
    }


# ---------------------------------------------------------------------- main
def generate_report(
    df: pd.DataFrame, cfg: dict[str, Any], window: Window, generated_at: datetime
) -> Path:
    figures_dir = resolve_path(cfg, "figures_dir")
    reports_dir = resolve_path(cfg, "reports_dir")
    figures_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    figs = _make_plots(df, figures_dir)
    dup = exact_duplicate_stats(df)
    synd = _syndication(df)
    near = _near_dup_summary(df)
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
        f"- **Window:** {window.start.date()} → {window.end.date()} "
        f"(Asia/Ho_Chi_Minh)\n"
        f"- **Articles:** {len(df)}  |  **Outlets:** {df['outlet'].nunique()}  |  "
        f"**Sections observed:** {df['section'].nunique(dropna=True)}\n"
        f"- **Segmentation:** {seg_methods} (token counts)\n")

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
    by_day = df.assign(d=_pub_date(df["publish_datetime"])).dropna(subset=["d"])
    if not by_day.empty:
        day_tbl = by_day.groupby("d").size().reset_index(name="articles")
        parts.append(_md_table(day_tbl))
    if "per_day" in figs:
        parts.append(f"\n![Articles per day]({rel(figs['per_day'])})\n")

    parts.append("\n## 4. Missingness by field (% null)\n")
    parts.append(_md_table(_missingness(df)))

    parts.append("\n## 5. Article length (Vietnamese word tokens)\n")
    parts.append(_md_table(_length_per_outlet(df)))
    if "mean_len" in figs:
        parts.append(f"\n![Mean length per outlet]({rel(figs['mean_len'])})\n")

    parts.append("\n## 6. Language\n")
    lang_tbl = lang_counts.reset_index()
    lang_tbl.columns = ["lang", "articles"]
    parts.append(_md_table(lang_tbl))
    parts.append(f"\n_Non-`vi` (flagged): {non_vi}._\n")

    parts.append("\n## 7. Duplication\n")
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
        parts.append(
            f"- Near-duplicate (same-story) copies: **{near['copies']}** "
            f"({100 * near['rate']:.1f}%), in **{near['clusters_multi']}** multi-article "
            f"clusters\n"
            f"- **Cross-outlet** same-story clusters: **{near['cross_outlet_clusters']}** "
            f"({near['articles_in_cross_outlet']} articles) — the syndication/overlap "
            f"signal that exact-hash misses\n")

    md = "\n".join(parts) + "\n"
    out = reports_dir / "quality_report.md"
    out.write_text(md, encoding="utf-8")
    _LOG.info("wrote data-quality report -> %s", out)
    return out
