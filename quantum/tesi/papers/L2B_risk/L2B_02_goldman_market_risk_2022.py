"""
Tutorial — Towards Quantum Advantage in Financial Market Risk — Goldman 2022
Slug: L2B_02_goldman_market_risk_2022
Level: L2B — Risk, Monte Carlo & derivatives

Run from repo root:
    python quantum/tesi/papers/L2B_risk/L2B_02_goldman_market_risk_2022.py
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
    """Estimate 95% VaR from linear P&L scenarios."""
    rng = np.random.default_rng(9)
    n = 20_000
    factors = rng.standard_normal((n, 3))
    weights = np.array([0.4, -0.2, 0.1])
    pnl = factors @ weights
    var_95 = -np.quantile(pnl, 0.05)
    explain("Linear toy P&L from three risk factors; 95% VaR as 5th percentile loss.")
    print(f"  scenarios = {n}")
    print(f"  95% VaR (loss positive) = {var_95:.4f}")
    print(f"  worst 1% mean (CVaR proxy) = {-pnl[pnl <= np.quantile(pnl, 0.01)].mean():.4f}")


def main() -> None:
    banner('Towards Quantum Advantage in Financial Market Risk — Goldman 2022', 'Towards quantum advantage in financial market risk')
    paper_info(
        'Towards Quantum Advantage in Financial Market Risk — Goldman 2022',
        'Resource estimates for VaR/CVaR with quantum speedup.',
        arxiv='2111.12509',
        level='L2B — Risk, Monte Carlo & derivatives',
    )

    section(1, "The Finance Problem")
    explain(
        'Market risk engines compute VaR and CVaR under many scenarios. Tight tails need enormous scenario counts.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Goldman analyzes resource requirements for quantum acceleration of risk metrics, comparing qubit counts and depths to classical clusters.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('VaR', 'Value at Risk: loss threshold at a confidence level.'),
        ('CVaR', 'Expected shortfall beyond the VaR threshold.'),
        ('Scenario generation', 'Simulating correlated market factors.'),
        ]
    )
    analogy('Risk engines are weather models for losses—quantum aims to forecast rare storms with fewer simulations.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Regulatory approval for quantum risk models is untested.',
        'Data governance limits cloud quantum use.',
        'Constant-factor overheads may dominate asymptotic gains.',
    )

    section(6, "Recap")
    recap(
        [
        "Goldman quantifies what 'advantage' might mean for risk.",
        'Tail metrics are the hardest and most interesting target.',
        'Resource estimates guide multi-year R&D planning.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Run L2B_03_qmc_risk_2024 tutorial.',
        'Try VaR demo below with more scenarios.',
        'Read counterparty credit risk 2025 paper.',
        ]
    )


if __name__ == "__main__":
    main()
