"""
Tutorial — Bank of Finland — Is the financial sector ready? 2025
Slug: L1_06_bof_finland_2025
Level: L1 — Industry surveys & policy

Run from repo root:
    python quantum/tesi/papers/L1_survey/L1_06_bof_finland_2025.py
"""
from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parents[2]))  # quantum/
sys.path.insert(0, str(_SCRIPT_DIR.parents[1]))  # quantum/tesi/

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _common import savefig

from _lib.beginner import (
    analogy,
    banner,
    concept_box,
    explain,
    next_steps,
    paper_info,
    recap,
    section,
)

def run_demo() -> None:
    """Simulate readiness scores across four pillars."""
    pillars = ["Talent", "Strategy", "Infrastructure", "PQC prep"]
    scores_2023 = np.array([0.35, 0.40, 0.30, 0.25])
    scores_2025 = np.array([0.50, 0.55, 0.45, 0.48])
    explain("Illustrative industry readiness (0–1) from survey-style data.")
    for p, s0, s1 in zip(pillars, scores_2023, scores_2025):
        print(f"  {p:16s} | 2023={s0:.2f} -> 2025={s1:.2f} (+{s1-s0:.2f})")
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(pillars))
    ax.bar(x - 0.2, scores_2023, 0.4, label="2023")
    ax.bar(x + 0.2, scores_2025, 0.4, label="2025")
    ax.set_xticks(x, pillars, rotation=15)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Readiness score")
    ax.set_title("Bank of Finland-style readiness pillars")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    path = savefig(fig, __file__, "bof_readiness.png")
    plt.close(fig)
    print(f"\n  Plot saved to: {path}")


def main() -> None:
    banner('Bank of Finland — Is the financial sector ready? 2025', 'Is the financial sector ready for quantum computing?')
    paper_info(
        'Bank of Finland — Is the financial sector ready? 2025',
        'Industry readiness survey; risks vs opportunities.',
        arxiv='',
        level='L1 — Industry surveys & policy',
    )

    section(1, "The Finance Problem")
    explain(
        'Central banks and supervisors worry about systemic readiness: skills, vendor dependence, crypto risk, and competitive asymmetry.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Bank of Finland survey synthesizes industry interviews and literature on readiness, opportunities, and threat scenarios including quantum attacks on banking infra.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Readiness index', 'Composite score across talent, strategy, infrastructure, and governance.'),
        ('Quantum threat horizon', 'Estimated years until cryptographically relevant quantum computers.'),
        ('Strategic optionality', 'Investing in pilots to avoid being locked out later.'),
        ]
    )
    analogy('The BoF report is a weather forecast for a storm that may arrive in 5–15 years—you still fix the roof now.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Survey samples may skew toward advanced institutions.',
        'Readiness scores are subjective.',
        'National contexts differ (EU vs US vs APAC).',
    )

    section(6, "Recap")
    recap(
        [
        'Industry readiness is uneven but improving.',
        'PQC and talent are common gaps.',
        'Supervisors want measured experimentation, not hype.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read FCA 2024 regulatory paper.',
        'Draft a one-page readiness checklist for a fictional bank.',
        'Explore PQC roadmap tutorial.',
        ]
    )


if __name__ == "__main__":
    main()
