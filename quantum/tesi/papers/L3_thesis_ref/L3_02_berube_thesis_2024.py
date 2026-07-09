"""
Tutorial — Pricing Options on Quantum Computers — Berube (Sherbrooke) 2024
Slug: L3_02_berube_thesis_2024
Level: L3 — Reference theses

Run from repo root:
    python quantum/tesi/papers/L3_thesis_ref/L3_02_berube_thesis_2024.py
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
    """Depth vs error tradeoff (toy model of thesis benchmark)."""
    depth = np.array([10, 20, 40, 80, 160])
    err_jauron = 0.02 + 0.0008 * depth
    err_berube = 0.02 + 0.0004 * depth
    explain("Illustrative pricing error vs circuit depth for two thesis generations.")
    for d, e1, e2 in zip(depth, err_jauron, err_berube):
        print(f"  depth={d:3d} | Jauron err={e1:.4f} | Berube err={e2:.4f}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(depth, err_jauron, "o-", label="Jauron 2022 (toy)")
    ax.plot(depth, err_berube, "s-", label="Berube 2024 (toy)")
    ax.set_xlabel("Circuit depth")
    ax.set_ylabel("Pricing error")
    ax.set_title("Thesis benchmark: depth vs error")
    ax.legend()
    ax.grid(alpha=0.3)
    path = savefig(fig, __file__, "thesis_depth_error.png")
    plt.close(fig)
    print(f"\n  Plot saved to: {path}")


def main() -> None:
    banner('Pricing Options on Quantum Computers — Berube (Sherbrooke) 2024', 'Extended thesis — improved circuits and benchmarks')
    paper_info(
        'Pricing Options on Quantum Computers — Berube (Sherbrooke) 2024',
        'Extended thesis with improved circuits and benchmarks.',
        arxiv='',
        level='L3 — Reference theses',
    )

    section(1, "The Finance Problem")
    explain(
        'Earlier thesis results may use deep circuits or optimistic assumptions. Berube 2024 refines circuits and benchmarks against updated hardware.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Improved state preparation, reduced depth, and systematic comparison to Jauron 2022 and classical baselines on larger instances.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Depth reduction', 'Fewer gates means less noise accumulation.'),
        ('Benchmark harness', 'Scripts that replay experiments with fixed seeds.'),
        ('Error mitigation', 'Post-processing to reduce bias from noise.'),
        ]
    )
    analogy("Berube is the director's cut—same story, tighter editing and better camera (circuits).")

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Still academic scale.',
        'Mitigation tricks may not generalize.',
        'Rapid hardware changes outdate specific numbers.',
    )

    section(6, "Recap")
    recap(
        [
        'Second thesis iterates on circuit efficiency.',
        'Compare fairly with fixed shot budgets.',
        'Treat depth as a first-class KPI.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Diff Berube vs Jauron workflow tables.',
        'Profile depth vs accuracy tradeoff in demo.',
        'Read Stamatopoulos industry paper for context.',
        ]
    )


if __name__ == "__main__":
    main()
