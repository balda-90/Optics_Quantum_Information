"""
Tutorial — Quantum computing for finance — Orus et al. 2019
Slug: L0_01_orus_2019
Level: L0 — Foundations

Run from repo root:
    python quantum/tesi/papers/L0_fondamenta/L0_01_orus_2019.py
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
    """Count finance tasks by suggested quantum approach (toy taxonomy)."""
    categories = {
        "Portfolio / QUBO": 4,
        "Derivatives / QAE": 3,
        "Risk / QMC": 3,
        "ML / QML": 2,
    }
    labels = list(categories.keys())
    counts = np.array(list(categories.values()), dtype=float)
    explain(
        "Below we simulate how a survey might tag finance tasks by algorithm family.",
        f"Total mapped tasks in this toy index: {int(counts.sum())}",
    )
    for label, c in zip(labels, counts):
        print(f"  {label:22s} -> {int(c)} papers/use-cases")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(labels, counts, color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"])
    ax.set_xlabel("Number of mapped use cases (illustrative)")
    ax.set_title("Orus-style mapping: finance task -> quantum family")
    ax.grid(axis="x", alpha=0.3)
    path = savefig(fig, __file__, "orus_finance_map.png")
    plt.close(fig)
    print(f"\n  Plot saved to: {path}")


def main() -> None:
    banner('Quantum computing for finance — Orus et al. 2019', 'Mapping finance problems to quantum algorithms')
    paper_info(
        'Quantum computing for finance — Orus et al. 2019',
        'Survey QC use cases in finance; map algorithms to problems.',
        arxiv='1807.03890',
        level='L0 — Foundations',
    )

    section(1, "The Finance Problem")
    explain(
        'Banks face many computationally heavy tasks: pricing exotic derivatives, optimizing large portfolios, simulating credit risk, and running anti-fraud models. Classical methods often scale poorly when accuracy requirements grow.',
        'Orus et al. (2019) ask a practical question: which finance problems are natural fits for quantum algorithms, and which are still far away?',
    )

    section(2, "What the Paper Proposes")
    explain(
        'The paper is a structured survey. It groups finance use cases (optimization, simulation, machine learning) and links each to quantum building blocks such as QAOA, VQE, amplitude estimation, and quantum annealing.',
        'Think of it as a roadmap index: not one algorithm, but a map from business pain points to quantum toolkits.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Combinatorial optimization', 'Choosing the best option among exponentially many discrete choices, like selecting assets in a portfolio.'),
        ('Quantum simulation', 'Using a controllable quantum system to mimic another hard-to-simulate system, such as stochastic market dynamics.'),
        ('Near-term vs fault-tolerant', "Today's noisy devices can run shallow circuits; fault-tolerant machines promise much larger algorithms later."),
        ]
    )
    analogy('Orus et al. is like a city transit map for quantum finance: it does not drive the train, but shows which line (algorithm family) reaches which destination (finance task).')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Survey papers summarize possibilities; they do not guarantee quantum advantage on real bank data today.',
        'Hardware noise and data encoding costs are often under-estimated in early roadmaps.',
        'Many cited speedups assume ideal oracles and fault-tolerant resources.',
    )

    section(6, "Recap")
    recap(
        [
        'Finance problems cluster into optimization, simulation, and learning.',
        'Quantum algorithms are matched by problem structure, not by hype.',
        'Orus 2019 is a foundational map for later applied papers.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        "Read Egger et al. 2020 for IBM's updated finance roadmap.",
        'Run script 01 in quantum/tesi/ for QAE error scaling intuition.',
        'Skim your portfolio optimization QUBO demo in quantum/tesi/03_portfolio_optimization_qubo.py.',
        ]
    )


if __name__ == "__main__":
    main()
