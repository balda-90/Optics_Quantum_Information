"""
Tutorial — End-to-End Portfolio Optimization with Quantum Annealing 2025
Slug: L2A_05_annealing_e2e_2025
Level: L2A — Portfolio optimization

Run from repo root:
    python quantum/tesi/papers/L2A_portfolio/L2A_05_annealing_e2e_2025.py
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
    """Simulated annealing on a 4-asset QUBO (toy e2e energy descent)."""
    mu = np.array([0.11, 0.09, 0.07, 0.06])
    Q = np.diag([0.025, 0.02, 0.018, 0.015])
    rng = np.random.default_rng(3)
    x = rng.integers(0, 2, size=4).astype(float)
    def energy(v):
        return float(mu @ v + v @ Q @ v)
    T = 1.0
    e = energy(x)
    explain("Start from random bitstring and cool temperature.")
    for step in range(8):
        i = rng.integers(0, 4)
        trial = x.copy()
        trial[i] = 1 - trial[i]
        et = energy(trial)
        if et < e or rng.random() < np.exp(-(et - e) / T):
            x, e = trial, et
        T *= 0.7
        print(f"  step {step+1}: x={x.astype(int)} energy={e:.4f} T={T:.3f}")
    print(f"\n  Final portfolio energy={e:.4f}")


def main() -> None:
    banner('End-to-End Portfolio Optimization with Quantum Annealing 2025', 'End-to-end portfolio optimization with quantum annealing')
    paper_info(
        'End-to-End Portfolio Optimization with Quantum Annealing 2025',
        'QUBO formulation solved via annealing.',
        arxiv='2504.08843',
        level='L2A — Portfolio optimization',
    )

    section(1, "The Finance Problem")
    explain(
        'Institutions want a full pipeline from market data to tradable weights using quantum annealers (e.g. D-Wave) as solvers.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Authors present QUBO derivation, embedding on annealing hardware, and classical validation of returned bitstrings.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Quantum annealing', 'Hardware finds low-energy states of an Ising/QUBO problem.'),
        ('Minor embedding', 'Mapping logical qubits to physical couplers on the chip.'),
        ('Chain breaks', 'Embedding artifacts that degrade solution quality.'),
        ]
    )
    analogy('Annealing is rolling a ball through a hilly landscape until it settles in the lowest valley (minimum energy).')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Limited connectivity on hardware graphs.',
        'Energy scale calibration is tricky.',
        'Competitive vs CPLEX/Gurobi on many instances.',
    )

    section(6, "Recap")
    recap(
        [
        'Annealing offers real hardware today for QUBOs.',
        'End-to-end means data, QUBO, embed, decode, validate.',
        'Check feasibility of returned portfolios.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Run quantum/tesi/03_portfolio_optimization_qubo.py.',
        'Compare IonQ gate-based large-scale paper.',
        'Study JPMorgan decomposition for size limits.',
        ]
    )


if __name__ == "__main__":
    main()
