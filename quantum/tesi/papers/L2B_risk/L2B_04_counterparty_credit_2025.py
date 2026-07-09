"""
Tutorial — Quantum Counterparty Credit Risk — Path-Dependent Derivatives 2025
Slug: L2B_04_counterparty_credit_2025
Level: L2B — Risk, Monte Carlo & derivatives

Run from repo root:
    python quantum/tesi/papers/L2B_risk/L2B_04_counterparty_credit_2025.py
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
    """Toy positive exposure on a capped payoff path."""
    rng = np.random.default_rng(5)
    n_paths, steps = 5000, 12
    paths = np.cumsum(rng.standard_normal((n_paths, steps)) * 0.01, axis=1)
    payoff = np.maximum(paths.max(axis=1) - 1.02, 0.0)
    exposure = payoff.mean()
    explain("Max-path trigger exposure (illustrative path-dependent structure).")
    print(f"  paths={n_paths}, steps={steps}")
    print(f"  mean positive exposure metric = {exposure:.6f}")
    print(f"  95th percentile exposure = {np.quantile(payoff, 0.95):.6f}")


def main() -> None:
    banner('Quantum Counterparty Credit Risk — Path-Dependent Derivatives 2025', 'Quantum counterparty credit risk for path-dependent derivatives')
    paper_info(
        'Quantum Counterparty Credit Risk — Path-Dependent Derivatives 2025',
        'Credit exposure simulation with quantum acceleration.',
        arxiv='2606.28701',
        level='L2B — Risk, Monte Carlo & derivatives',
    )

    section(1, "The Finance Problem")
    explain(
        'Counterparty exposure on path-dependent trades depends on many future market paths and netting sets—expensive to simulate classically.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Authors explore quantum acceleration for exposure profiles and CVA-like metrics on path-dependent structures.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Exposure profile', 'Expected positive exposure over time buckets.'),
        ('CVA', 'Credit Valuation Adjustment: price of counterparty default risk.'),
        ('Path dependence', 'Payoff depends on entire trajectory, not just terminal price.'),
        ]
    )
    analogy('Counterparty risk is measuring how much rope you lent out on a windy day—paths matter, not just the final position.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Netting and collateral rules complicate oracles.',
        'Legal and data heterogeneity across desks.',
        'Quantum advantage unproven with real netting sets.',
    )

    section(6, "Recap")
    recap(
        [
        'Path-dependent exposure is a natural MC target.',
        'Quantum aims at scenario count reduction.',
        'Credit risk integration is harder than single-name options.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Review Stamatopoulos option pricing baseline.',
        'Simulate exposure profiles classically first.',
        'Read Goldman market risk for resource context.',
        ]
    )


if __name__ == "__main__":
    main()
