"""
Tutorial — Scaling VQE for Dynamic Portfolio Optimization — BBVA/IBM 2025
Slug: L2A_02_bbva_vqe_2025
Level: L2A — Portfolio optimization

Run from repo root:
    python quantum/tesi/papers/L2A_portfolio/L2A_02_bbva_vqe_2025.py
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
    """Brute-force minimize a 2-asset QUBO for three risk-aversion values."""
    mu = np.array([0.12, 0.08])
    cov = np.array([[0.04, 0.01], [0.01, 0.02]])
    lambdas = [0.5, 1.0, 2.0]
    explain("Search binary inclusion x in {0,1}^2 minimizing mu^T x + lambda x^T cov x.")
    for lam in lambdas:
        best_e, best_x = np.inf, None
        for x0 in (0, 1):
            for x1 in (0, 1):
                x = np.array([x0, x1], dtype=float)
                e = mu @ x + lam * x @ cov @ x
                if e < best_e:
                    best_e, best_x = e, x
        print(f"  lambda={lam:.1f} -> x={best_x.astype(int)} energy={best_e:.4f}")


def main() -> None:
    banner('Scaling VQE for Dynamic Portfolio Optimization — BBVA/IBM 2025', 'Scaling VQE for dynamic portfolio optimization')
    paper_info(
        'Scaling VQE for Dynamic Portfolio Optimization — BBVA/IBM 2025',
        'VQE for dynamic constraints and rebalancing.',
        arxiv='2412.19150',
        level='L2A — Portfolio optimization',
    )

    section(1, "The Finance Problem")
    explain(
        'Portfolios change with market conditions, transaction costs, and regulatory limits. Static solutions decay quickly.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'BBVA and IBM study VQE for dynamic portfolio problems with constraints, testing parameter transfer and circuit depth on hardware.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('VQE', 'Variational Quantum Eigensolver minimizes energy of a Hamiltonian encoding the objective.'),
        ('Parameter transfer', "Warm-starting VQE from previous day's solution."),
        ('Constraint penalty', 'Encoding limits as penalty terms in the Hamiltonian.'),
        ]
    )
    analogy('VQE is tuning a radio antenna: small knob turns (parameters) until the signal (portfolio cost) is strongest.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Barren plateaus and noise hurt convergence.',
        'Dynamic constraints increase circuit complexity.',
        'Beat classical heuristics only on selected instances.',
    )

    section(6, "Recap")
    recap(
        [
        'VQE is a flagship hybrid approach for portfolio opt.',
        'Dynamic rebalancing needs warm-start strategies.',
        'BBVA work bridges bank requirements and IBM hardware.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Compare annealing e2e paper L2A_05.',
        'Study PO-QA unified framework.',
        'Encode a 2-asset QUBO manually in the demo.',
        ]
    )


if __name__ == "__main__":
    main()
