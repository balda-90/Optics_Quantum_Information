"""
Script 03 — Portfolio optimization (Markowitz vs QUBO formulation)
Literature: Level 2A papers (JPMorgan 2025, PO-QA, quantum annealing)

Objective replicated:
  1) Solve a small mean-variance portfolio classically (Markowitz).
  2) Search a discrete weight grid (QUBO/annealing-friendly encoding).

Run:
  python quantum/tesi/03_portfolio_optimization_qubo.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from scipy.optimize import minimize

from _common import banner

ASSETS = ["A", "B", "C"]
MU = np.array([0.10, 0.12, 0.08])
COV = np.array([
    [0.04, 0.006, 0.004],
    [0.006, 0.05, 0.005],
    [0.004, 0.005, 0.03],
])
RISK_AVERSION = 2.0
WEIGHT_LEVELS = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
PENALTY = 50.0


def portfolio_cost(w: np.ndarray) -> float:
    return 0.5 * RISK_AVERSION * w @ COV @ w - MU @ w


def markowitz_weights() -> np.ndarray:
    n = len(MU)

    def objective(w: np.ndarray) -> float:
        return portfolio_cost(w)

    cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    bounds = [(0.0, 1.0)] * n
    w0 = np.ones(n) / n
    res = minimize(objective, w0, bounds=bounds, constraints=cons)
    return res.x


def best_discrete_qubo() -> np.ndarray:
    """Brute-force discrete weights — same objective + budget penalty as QUBO."""
    best_w = None
    best_val = np.inf
    for w0 in WEIGHT_LEVELS:
        for w1 in WEIGHT_LEVELS:
            for w2 in WEIGHT_LEVELS:
                w = np.array([w0, w1, w2])
                val = portfolio_cost(w) + PENALTY * (w.sum() - 1.0) ** 2
                if val < best_val:
                    best_val = val
                    best_w = w
    assert best_w is not None
    return best_w


def main() -> None:
    banner("Portfolio optimization — Markowitz vs QUBO (discrete)")

    w_classical = markowitz_weights()
    print("Classical Markowitz (continuous weights):")
    for name, w in zip(ASSETS, w_classical):
        print(f"  {name}: {w:.3f}")
    print(f"  Expected return: {MU @ w_classical:.4f}")
    print(f"  Variance: {w_classical @ COV @ w_classical:.6f}")

    w_qubo = best_discrete_qubo()
    print("\nBest discrete QUBO-style solution (quantum-annealing friendly):")
    for name, w in zip(ASSETS, w_qubo):
        print(f"  {name}: {w:.3f}")
    print(f"  Expected return: {MU @ w_qubo:.4f}")
    print(f"  Variance: {w_qubo @ COV @ w_qubo:.6f}")

    print("\nDone. Full papers use larger QUBO + quantum annealing / VQE (Level 2A).")


if __name__ == "__main__":
    main()
