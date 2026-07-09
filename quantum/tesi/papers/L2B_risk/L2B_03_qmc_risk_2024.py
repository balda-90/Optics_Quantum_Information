"""
Tutorial — Quantum Monte Carlo for financial risk analytics 2024
Slug: L2B_03_qmc_risk_2024
Level: L2B — Risk, Monte Carlo & derivatives

Run from repo root:
    python quantum/tesi/papers/L2B_risk/L2B_03_qmc_risk_2024.py
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
    """Compare MC vs ideal QAE queries for tail probability p=0.05."""
    p = 0.05
    eps = 0.005
    classical_n = int(np.ceil(1 / eps**2))
    qae_n = int(np.ceil(1 / eps))
    explain(f"Target tail probability p={p}, precision eps={eps}.")
    print(f"  classical samples ~ O(1/eps^2) = {classical_n}")
    print(f"  ideal QAE queries ~ O(1/eps) = {qae_n}")
    print(f"  ratio classical/QAE ~ {classical_n/qae_n:.1f}x")


def main() -> None:
    banner('Quantum Monte Carlo for financial risk analytics 2024', 'Quantum Monte Carlo for financial risk analytics')
    paper_info(
        'Quantum Monte Carlo for financial risk analytics 2024',
        'End-to-end QMC pipeline for risk metrics.',
        arxiv='2404.03035',
        level='L2B — Risk, Monte Carlo & derivatives',
    )

    section(1, "The Finance Problem")
    explain(
        'Risk teams need end-to-end pipelines producing VaR, CVaR, and stress metrics under tight latency budgets.',
    )

    section(2, "What the Paper Proposes")
    explain(
        '2024 QMC work describes integrating quantum subroutines for tail probability estimation inside risk analytics stacks.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Tail probability', 'Rare-event frequency driving VaR/CVaR.'),
        ('QMC pipeline', 'Data ingest -> scenario gen -> quantum estimate -> validation.'),
        ('Backtesting', 'Checking VaR exceptions on historical data.'),
        ]
    )
    analogy('QMC risk is replacing the slowest gear in a watch—the tail estimator—while keeping the case and dial classical.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Production risk systems are heavily regulated and validated.',
        'Quantum modules must pass same backtesting as classical.',
        'End-to-end advantage unproven on real books.',
    )

    section(6, "Recap")
    recap(
        [
        'Focus on tail metrics where MC is expensive.',
        'Pipeline thinking beats isolated circuit demos.',
        'Validation and governance are as hard as physics.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Extend Goldman resource estimates with your book size.',
        'Run counterparty credit tutorial.',
        'Practice backtesting VaR on historical series.',
        ]
    )


if __name__ == "__main__":
    main()
