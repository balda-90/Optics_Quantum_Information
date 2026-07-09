"""
Tutorial — Large-scale portfolio optimization on trapped-ion QC — IonQ 2026
Slug: L2A_06_ionq_large_scale_2026
Level: L2A — Portfolio optimization

Run from repo root:
    python quantum/tesi/papers/L2A_portfolio/L2A_06_ionq_large_scale_2026.py
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _common import savefig

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
    """Project solution quality vs number of assets (toy scaling curve)."""
    assets = np.array([4, 8, 16, 32, 64])
    classical_gap = 0.02 * np.log(assets)  # % above best
    ionq_gap = 0.05 + 0.03 * np.log(assets)
    explain("Gap to best-known objective (lower is better) — illustrative only.")
    for a, cg, ig in zip(assets, classical_gap, ionq_gap):
        print(f"  n={a:2d} assets | classical heuristic gap={cg*100:.1f}% | ionq demo gap={ig*100:.1f}%")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(assets, classical_gap * 100, "o-", label="Classical heuristic")
    ax.plot(assets, ionq_gap * 100, "s-", label="Trapped-ion demo")
    ax.set_xlabel("Number of assets")
    ax.set_ylabel("Optimality gap (%)")
    ax.set_title("Large-scale portfolio scaling (toy)")
    ax.legend()
    ax.grid(alpha=0.3)
    path = savefig(fig, __file__, "ionq_scaling.png")
    plt.close(fig)
    print(f"\n  Plot saved to: {path}")


def main() -> None:
    banner('Large-scale portfolio optimization on trapped-ion QC — IonQ 2026', 'Large-scale portfolio optimization on trapped-ion hardware')
    paper_info(
        'Large-scale portfolio optimization on trapped-ion QC — IonQ 2026',
        'Hardware demonstration at scale.',
        arxiv='2602.23976',
        level='L2A — Portfolio optimization',
    )

    section(1, "The Finance Problem")
    explain(
        'Gate-based machines are improving qubit counts and connectivity. Can they run portfolio instances beyond toy size?',
    )

    section(2, "What the Paper Proposes")
    explain(
        'IonQ 2026 demonstration scales portfolio QUBO instances on trapped-ion devices, reporting solution quality vs classical heuristics.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Trapped-ion QC', 'Qubits stored in ions manipulated by lasers; often high fidelity.'),
        ('Circuit depth', 'Number of gate layers; affects noise accumulation.'),
        ('Solution quality', 'Objective value vs best known classical baseline.'),
        ]
    )
    analogy('Scaling qubits is like expanding an orchestra—more musicians only help if they stay in time (low noise).')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Queue times and cost for cloud access.',
        'Instance sizes still below daily production universes.',
        'Fair classical tuning may narrow reported gaps.',
    )

    section(6, "Recap")
    recap(
        [
        'Hardware demos prove growing capability.',
        'Compare fairly against strong classical baselines.',
        'IonQ paper anchors gate-based portfolio scaling.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read JPMorgan decomposition for when hardware is still too small.',
        'Track circuit depth vs error in L3 thesis tutorials.',
        'Benchmark your own QUBO on cloud IonQ if available.',
        ]
    )


if __name__ == "__main__":
    main()
