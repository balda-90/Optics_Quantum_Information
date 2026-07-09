"""
Tutorial — Decomposition pipeline for large-scale portfolio optimization — JPMorgan 2025
Slug: L2A_01_jpmorgan_decomposition_2025
Level: L2A — Portfolio optimization

Run from repo root:
    python quantum/tesi/papers/L2A_portfolio/L2A_01_jpmorgan_decomposition_2025.py
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
    """Partition a 6-asset covariance matrix into two QUBO blocks."""
    rng = np.random.default_rng(11)
    n = 6
    A = rng.standard_normal((n, n))
    cov = A @ A.T
    block_a = cov[:3, :3]
    block_b = cov[3:, 3:]
    explain("Toy 6-asset universe split into two 3-asset blocks.")
    print("  Block A diagonal (variances):", np.round(np.diag(block_a), 4))
    print("  Block B diagonal (variances):", np.round(np.diag(block_b), 4))
    cross = cov[:3, 3:]
    print("  Cross-block coupling Frobenius norm:", float(np.linalg.norm(cross, "fro")))


def main() -> None:
    banner('Decomposition pipeline for large-scale portfolio optimization — JPMorgan 2025', 'Decomposition pipeline for large-scale portfolio optimization')
    paper_info(
        'Decomposition pipeline for large-scale portfolio optimization — JPMorgan 2025',
        'Decompose large portfolios for hybrid quantum solvers.',
        arxiv='2409.10301',
        level='L2A — Portfolio optimization',
    )

    section(1, "The Finance Problem")
    explain(
        'Real portfolios may have thousands of assets. A monolithic QUBO is too large for current quantum hardware.',
        'JPMorgan proposes decomposing the problem into smaller blocks solved hybridly and reassembled.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Use clustering or graph partitioning on the covariance structure, solve sub-QUBOs on quantum/annealing devices, then coordinate classically.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Block decomposition', 'Splitting a large problem into manageable subproblems.'),
        ('Coupling matrix', 'Covariance or constraint links between assets.'),
        ('Hybrid coordinator', 'Classical layer that merges sub-solutions and enforces global constraints.'),
        ]
    )
    analogy('Like solving a giant jigsaw by working on corners and color clusters first, then fitting them together.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Decomposition can sacrifice global optimality.',
        'Interface constraints between blocks need careful tuning.',
        'Still needs classical heavy lifting for data and validation.',
    )

    section(6, "Recap")
    recap(
        [
        'Scale is the main obstacle for quantum portfolio opt.',
        'Decomposition is a practical engineering strategy.',
        'JPMorgan pipeline targets institution-sized universes.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Try BBVA VQE tutorial for dynamic constraints.',
        'Run quantum/tesi/03_portfolio_optimization_qubo.py.',
        'Read IonQ 2026 large-scale demo paper.',
        ]
    )


if __name__ == "__main__":
    main()
