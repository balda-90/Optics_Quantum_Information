"""
Script 04 — Industry survey themes (Bank of Finland 2025)
Literature: Bank of Finland Bulletin (2025) + papers_catalog.yaml

Objective replicated:
  Extract key themes from the local HTML survey article and map them to
  the thesis paper levels (foundations, portfolio, risk, PQC, QML).

Run:
  python quantum/tesi/04_industry_survey_themes.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import banner, savefig
from _lib.catalog import load_catalog, list_local_pdfs, summarize_catalog, thesis_data_dir


def extract_bof_headings(html_path: Path) -> list[str]:
    if not html_path.exists():
        return []
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    # Main section titles appear in the article sidebar
    side = re.findall(
        r'class="side-menu-text[^"]*"[^>]*>(.*?)</span>',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    clean_side = [re.sub(r"<[^>]+>", "", h).strip() for h in side]
    clean_side = list(dict.fromkeys(c for c in clean_side if len(c) > 20))

    raw_h2 = re.findall(r"<h2[^>]*>(.*?)</h2>", text, flags=re.IGNORECASE | re.DOTALL)
    clean_h2 = [re.sub(r"<[^>]+>", "", h).strip() for h in raw_h2]
    clean_h2 = [c for c in clean_h2 if c.lower() not in {"notes", "keywords"}]

    return clean_side or clean_h2


def main() -> None:
    banner("Thesis literature — industry survey themes")

    catalog = load_catalog()
    counts = summarize_catalog(catalog)
    data_dir = thesis_data_dir()
    pdfs = list_local_pdfs(data_dir)

    print(f"Data folder: {data_dir}")
    print(f"Local PDFs found: {len(pdfs)}")
    print("\nPapers per level (from catalog):")
    for level in catalog["levels"]:
        n = counts[level["id"]]
        print(f"  {level['id']} {level['title']}: {n} papers")
        print(f"      themes: {', '.join(level['themes'])}")

    html = data_dir / "Livello_1_Survey_Industry" / (
        "Bank of Finland Quantum computing is coming financial sector ready 2025.html"
    )
    headings = extract_bof_headings(html)
    print("\nBank of Finland (2025) — section headings:")
    for h in headings:
        print(f"  • {h}")

    labels = [f"{lv['id']}\n{lv['title'][:18]}" for lv in catalog["levels"]]
    values = [counts[lv["id"]] for lv in catalog["levels"]]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color="steelblue")
    ax.set_ylabel("Number of papers (catalog)")
    ax.set_title("Thesis bibliography structure (data/100_TESI)")
    ax.grid(True, axis="y", alpha=0.3)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()

    path = savefig(fig, __file__, "thesis_catalog_by_level.png")
    plt.close(fig)
    print(f"\nPlot saved to: {path}")
    print("\nDone. Open 00_thesis_literature_map.ipynb for interactive exploration.")


if __name__ == "__main__":
    main()
