"""
Script 02 — European option pricing (classical Monte Carlo baseline)
Literature: Stamatopoulos et al. (2020); Rebentrost et al. (2018)

Objective replicated:
  Price a European call under GBM via Monte Carlo — the classical baseline
  that QAE-based quantum algorithms aim to accelerate.

Run:
  python quantum/tesi/02_european_option_monte_carlo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import banner, savefig

# Market parameters (Stamatopoulos-style toy example)
S0 = 100.0
K = 100.0
r = 0.05
sigma = 0.2
T = 1.0


def black_scholes_call(S0: float, K: float, r: float, sigma: float, T: float) -> float:
    from scipy.stats import norm

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def mc_european_call(
    n_paths: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    """Return (price estimate, standard error)."""
    z = rng.standard_normal(n_paths)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
    payoffs = np.maximum(ST - K, 0.0)
    discounted = np.exp(-r * T) * payoffs
    price = discounted.mean()
    stderr = discounted.std(ddof=1) / np.sqrt(n_paths)
    return float(price), float(stderr)


def main() -> None:
    banner("European call — classical Monte Carlo")

    analytical = black_scholes_call(S0, K, r, sigma, T)
    print(f"Black-Scholes analytical price: {analytical:.4f}")

    rng = np.random.default_rng(7)
    path_counts = np.logspace(2, 5, 12, dtype=int)
    path_counts = np.unique(path_counts)

    estimates = []
    stderrs = []
    for n in path_counts:
        price, se = mc_european_call(int(n), rng)
        estimates.append(price)
        stderrs.append(se)
        print(f"  N={n:>6} -> price={price:.4f}  stderr={se:.4f}")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogx(path_counts, estimates, "o-", label="MC estimate")
    ax.axhline(analytical, color="C1", ls="--", label=f"Black-Scholes ({analytical:.3f})")
    ax.fill_between(
        path_counts,
        np.array(estimates) - 2 * np.array(stderrs),
        np.array(estimates) + 2 * np.array(stderrs),
        alpha=0.2,
        label="±2σ MC band",
    )
    ax.set_xlabel("Number of Monte Carlo paths")
    ax.set_ylabel("Call option price")
    ax.set_title("Classical MC baseline for quantum option pricing papers")
    ax.legend()
    ax.grid(True, alpha=0.3)

    path = savefig(fig, __file__, "european_call_mc.png")
    plt.close(fig)
    print(f"\nPlot saved to: {path}")
    print("\nDone. Quantum papers replace this sampling step with QAE (script 01).")


if __name__ == "__main__":
    main()
