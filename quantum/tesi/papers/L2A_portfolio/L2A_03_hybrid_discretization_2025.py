"""
Tutorial — Multiple Discretization Portfolio Optimization — Hybrid 2025
Slug: L2A_03_hybrid_discretization_2025
Level: L2A — Portfolio optimization

Run from repo root:
    python quantum/tesi/papers/L2A_portfolio/L2A_03_hybrid_discretization_2025.py
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
    """Compare 2-bit vs 3-bit weight grids for one asset (toy)."""
    levels2 = np.array([0.0, 0.33, 0.67, 1.0])
    levels3 = np.array([i / 7 for i in range(8)])
    target = 0.55
    w2 = levels2[np.argmin(np.abs(levels2 - target))]
    w3 = levels3[np.argmin(np.abs(levels3 - target))]
    explain(f"Target weight {target:.2f} on a single asset slot.")
    print(f"  2-bit grid nearest: {w2:.4f} (error {abs(w2-target):.4f})")
    print(f"  3-bit grid nearest: {w3:.4f} (error {abs(w3-target):.4f})")
    print(f"  Qubit cost: 2-bit needs 2 qubits/asset; 3-bit needs 3 qubits/asset.")


def main() -> None:
    banner('Multiple Discretization Portfolio Optimization — Hybrid 2025', 'Hybrid classical-quantum portfolio opt with discretized weights')
    paper_info(
        'Multiple Discretization Portfolio Optimization — Hybrid 2025',
        'Hybrid classical-quantum with discretized weights.',
        arxiv='',
        level='L2A — Portfolio optimization',
    )

    section(1, "The Finance Problem")
    explain(
        'Continuous portfolio weights must be discretized for QUBO encodings. Too few levels lose precision; too many blow up qubit count.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Hybrid pipeline: classical search over coarse grids, quantum solver for combinatorial subproblems, iterative refinement of discretization.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Discretization', 'Mapping continuous weights to finite bit strings.'),
        ('Hybrid loop', 'Alternating classical refinement and quantum solve.'),
        ('Precision-qubit tradeoff', 'More bits per asset increases problem size exponentially.'),
        ]
    )
    analogy('Like approximating a smooth curve with step sizes—you refine the steps where the curve bends most (active assets).')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Discretization gap vs continuous optimum.',
        'Multiple passes increase total runtime.',
        'Hardware limits cap bits per asset.',
    )

    section(6, "Recap")
    recap(
        [
        'Discretization is unavoidable for QUBO portfolios.',
        'Hybrid refinement mitigates coarse grids.',
        'Track gap to continuous classical solution.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read JPMorgan decomposition for scaling.',
        'Run annealing e2e tutorial.',
        'Try 3-level weight encoding on paper.',
        ]
    )


if __name__ == "__main__":
    main()
