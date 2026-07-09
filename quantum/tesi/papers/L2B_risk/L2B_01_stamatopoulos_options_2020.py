"""
Tutorial — Option Pricing using Quantum Computers — Stamatopoulos (JPMorgan) 2020
Slug: L2B_01_stamatopoulos_options_2020
Level: L2B — Risk, Monte Carlo & derivatives

Run from repo root:
    python quantum/tesi/papers/L2B_risk/L2B_01_stamatopoulos_options_2020.py
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
from scipy.stats import norm

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
    """Price a European call via MC and compare to Black-Scholes."""
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    n = 50_000
    rng = np.random.default_rng(21)
    z = rng.standard_normal(n)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
    payoffs = np.maximum(ST - K, 0.0)
    mc_price = np.exp(-r * T) * payoffs.mean()
    se = np.exp(-r * T) * payoffs.std(ddof=1) / np.sqrt(n)
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    bs = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    explain("Toy Stamatopoulos baseline: MC vs analytic Black-Scholes.")
    print(f"  MC price = {mc_price:.4f} +/- {1.96*se:.4f} (95% CI)")
    print(f"  Black-Scholes = {bs:.4f}")
    print(f"  ITM probability estimate = {(payoffs > 0).mean():.4f}")


def main() -> None:
    banner('Option Pricing using Quantum Computers — Stamatopoulos (JPMorgan) 2020', 'Option pricing using quantum computers (JPMorgan)')
    paper_info(
        'Option Pricing using Quantum Computers — Stamatopoulos (JPMorgan) 2020',
        'QAE for European option pricing under GBM.',
        arxiv='1905.02666',
        level='L2B — Risk, Monte Carlo & derivatives',
    )

    section(1, "The Finance Problem")
    explain(
        'European and path-dependent options under stochastic volatility models require many Monte Carlo paths for tight confidence intervals.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Stamatopoulos et al. detail a quantum pipeline for European options: state preparation, payoff oracle, and QAE for price estimation.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('GBM', 'Geometric Brownian Motion baseline for equity underlyings.'),
        ('Payoff oracle', 'Quantum circuit marking paths with positive option payoff.'),
        ('Price from amplitude', 'Option price linked to estimated payoff probability/amplitude.'),
        ]
    )
    analogy('QAE option pricing counts winning lottery tickets (ITM paths) with fewer draws than classical sampling.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Log-normal assumptions break in crises.',
        'Oracle construction for exotic payoffs is hard.',
        'Practical speedup not yet demonstrated at bank scale.',
    )

    section(6, "Recap")
    recap(
        [
        'Stamatopoulos is the canonical bank option + QAE reference.',
        'Classical MC remains the production baseline.',
        'QAE targets the statistical error bottleneck.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Run quantum/tesi/02_european_option_monte_carlo.py.',
        'Read Jauron thesis tutorial L3_01.',
        'Study Rebentrost MC 2018 foundations.',
        ]
    )


if __name__ == "__main__":
    main()
