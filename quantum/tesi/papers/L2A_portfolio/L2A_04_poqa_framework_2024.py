"""
Tutorial — PO-QA Framework — Portfolio Optimization with Quantum Algorithms 2024
Slug: L2A_04_poqa_framework_2024
Level: L2A — Portfolio optimization

Run from repo root:
    python quantum/tesi/papers/L2A_portfolio/L2A_04_poqa_framework_2024.py
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
    """Same QUBO, two solver scores (QAOA vs annealing) on 3-asset toy."""
    mu = np.array([0.10, 0.07, 0.05])
    Q = np.diag([0.03, 0.02, 0.015])
    best = []
    for x0 in (0, 1):
        for x1 in (0, 1):
            for x2 in (0, 1):
                x = np.array([x0, x1, x2], dtype=float)
                e = mu @ x + x @ Q @ x
                best.append((e, x))
    best.sort(key=lambda t: t[0])
    e_opt, x_opt = best[0]
    qaoa_score = e_opt * 1.05  # noisy solver
    anneal_score = e_opt * 1.02
    explain("Optimal energy vs illustrative QAOA/annealer outputs on same instance.")
    print(f"  optimum x={x_opt.astype(int)} energy={e_opt:.4f}")
    print(f"  QAOA reported energy={qaoa_score:.4f} (gap {(qaoa_score/e_opt-1)*100:.1f}%)")
    print(f"  Annealer reported energy={anneal_score:.4f} (gap {(anneal_score/e_opt-1)*100:.1f}%)")


def main() -> None:
    banner('PO-QA Framework — Portfolio Optimization with Quantum Algorithms 2024', 'PO-QA unified framework for quantum portfolio algorithms')
    paper_info(
        'PO-QA Framework — Portfolio Optimization with Quantum Algorithms 2024',
        'Unified framework for quantum portfolio algorithms.',
        arxiv='2407.19857',
        level='L2A — Portfolio optimization',
    )

    section(1, "The Finance Problem")
    explain(
        'Teams face a maze of QAOA, VQE, annealing, and hybrid variants without a common interface to compare them fairly.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'PO-QA proposes a unified formulation: encode portfolio problems once, plug in different quantum solvers, standardize metrics and benchmarks.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('QAOA', 'Quantum Approximate Optimization Algorithm alternates cost and mixer layers.'),
        ('Solver adapter', 'Common API wrapping distinct quantum backends.'),
        ('Benchmark suite', 'Shared instances and KPIs (Sharpe, turnover, runtime).'),
        ]
    )
    analogy('PO-QA is USB-C for portfolio solvers—one plug shape, many devices.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Framework overhead may hide solver-specific tricks.',
        'Fair tuning budget across solvers is debatable.',
        'Still early for production risk systems.',
    )

    section(6, "Recap")
    recap(
        [
        'Unification helps reproducible comparisons.',
        'Encode once, swap quantum backend.',
        'PO-QA is methodological glue for L2A papers.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Run annealing vs QAOA toy demo below.',
        'Pick two papers and compare via PO-QA lens.',
        'Document KPIs before benchmarking.',
        ]
    )


if __name__ == "__main__":
    main()
