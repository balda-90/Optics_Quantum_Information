"""
Script 01 — Quantum Amplitude Estimation (QAE)
Literature: Brassard et al. (2002); Rebentrost et al. (2018); Stamatopoulos (2020)

Objective replicated:
  Compare statistical error when estimating a probability p using
  classical Monte Carlo (error ~ 1/sqrt(N)) vs ideal QAE (error ~ 1/N).

Run:
  python quantum/tesi/01_quantum_amplitude_estimation.py
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

# True probability to estimate (e.g. probability of payoff > 0 in a derivative simulation)
P_TRUE = 0.37
SHOTS_LIST = np.array([10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
N_TRIALS = 200


def classical_mc_error(shots: int, rng: np.random.Generator) -> float:
    """Mean absolute error over trials for classical sampling."""
    errors = []
    for _ in range(N_TRIALS):
        samples = rng.random(shots) < P_TRUE
        p_hat = samples.mean()
        errors.append(abs(p_hat - P_TRUE))
    return float(np.mean(errors))


def ideal_qae_error(shots: int) -> float:
    """
    Ideal QAE scaling (Brassard): error ~ pi / (2 * shots) for amplitude a in (0,1).
    We use this as the theoretical target curve, not a full Grover implementation.
    """
    return np.pi / (2 * shots)


def main() -> None:
    banner("QAE vs Classical MC — error scaling")

    rng = np.random.default_rng(42)
    mc_errors = [classical_mc_error(int(s), rng) for s in SHOTS_LIST]
    qae_errors = [ideal_qae_error(int(s)) for s in SHOTS_LIST]
    classical_bound = 1 / np.sqrt(SHOTS_LIST)

    print(f"Target probability p = {P_TRUE}")
    print("\nSample errors (shots -> MC error, QAE bound):")
    for s, mc, qae in zip(SHOTS_LIST[:5], mc_errors[:5], qae_errors[:5]):
        print(f"  {s:>5} -> MC {mc:.4f} | QAE bound {qae:.4f}")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(SHOTS_LIST, mc_errors, "o-", label="Classical MC (simulated)")
    ax.loglog(SHOTS_LIST, classical_bound * np.sqrt(P_TRUE * (1 - P_TRUE)), "--", label=r"Classical ~ $1/\sqrt{N}$")
    ax.loglog(SHOTS_LIST, qae_errors, "s-", label=r"Ideal QAE ~ $1/N$")
    ax.set_xlabel("Number of samples / oracle queries")
    ax.set_ylabel("Mean absolute error on p")
    ax.set_title("Why QAE matters for finance (Rebentrost / Stamatopoulos)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()

    path = savefig(fig, __file__, "qae_vs_mc_scaling.png")
    plt.close(fig)
    print(f"\nPlot saved to: {path}")
    print("\nDone. Next: European option pricing with classical MC (script 02).")


if __name__ == "__main__":
    main()
