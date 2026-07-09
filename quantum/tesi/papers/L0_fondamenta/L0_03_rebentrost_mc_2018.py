"""
Tutorial — Quantum computational finance — Monte Carlo pricing — Rebentrost 2018
Slug: L0_03_rebentrost_mc_2018
Level: L0 — Foundations

Run from repo root:
    python quantum/tesi/papers/L0_fondamenta/L0_03_rebentrost_mc_2018.py
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
    """Compare classical MC error scaling vs ideal QAE bound."""
    p_true = 0.42
    shots = np.array([20, 50, 100, 200, 500, 1000, 2000])
    rng = np.random.default_rng(7)
    mc_errors = []
    for s in shots:
        trials = [abs((rng.random(s) < p_true).mean() - p_true) for _ in range(300)]
        mc_errors.append(float(np.mean(trials)))
    qae_bound = np.pi / (2 * shots)
    explain(f"Estimating probability p={p_true} (e.g. ITM indicator).")
    print("\n  shots | MC error | QAE bound")
    for s, mc, qae in zip(shots[::2], mc_errors[::2], qae_bound[::2]):
        print(f"  {s:5d} | {mc:.4f}   | {qae:.4f}")
    ratio = mc_errors[-1] / qae_bound[-1]
    print(f"\n  At {shots[-1]} shots, MC error is ~{ratio:.1f}x the ideal QAE bound.")


def main() -> None:
    banner('Quantum computational finance — Monte Carlo pricing — Rebentrost 2018', 'Quantum Monte Carlo pricing with amplitude estimation')
    paper_info(
        'Quantum computational finance — Monte Carlo pricing — Rebentrost 2018',
        'QAE-based speedup for derivative pricing vs classical MC.',
        arxiv='1805.00109',
        level='L0 — Foundations',
    )

    section(1, "The Finance Problem")
    explain(
        'Derivative pricing often relies on Monte Carlo simulation. To reduce pricing error by a factor of 10, classical MC typically needs 100× more samples because error scales like 1/√N.',
        'For exotics and multi-asset products, this becomes expensive in production risk engines.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Rebentrost et al. (2018) combine quantum state preparation with Quantum Amplitude Estimation (QAE) to estimate expected payoffs.',
        'The promise is a query complexity scaling closer to 1/N instead of 1/√N, which is highly attractive for risk-sensitive pricing.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Quantum Monte Carlo', 'Encode random scenarios in superposition and estimate payoff amplitudes.'),
        ('Oracle', 'A quantum subroutine that marks states where a condition (e.g. positive payoff) holds.'),
        ('Quadratic speedup', 'QAE can reduce sample/oracle queries quadratically vs classical MC in ideal settings.'),
        ]
    )
    analogy('Classical MC is like polling random voters one-by-one; QAE is like a clever counting algorithm that extracts the election result with fewer questions—if the polling machine is perfect.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Loading financial distributions into quantum states is costly.',
        'Current hardware cannot run full fault-tolerant QAE at scale.',
        'Constant factors and error correction overhead may erode speedups.',
    )

    section(6, "Recap")
    recap(
        [
        'Rebentrost 2018 connects derivative pricing to QAE.',
        'The headline is better scaling in oracle queries.',
        'State preparation is often the hidden bottleneck.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Run L0_04_brassard_qae_2002 for the original QAE theory.',
        'Run quantum/tesi/02_european_option_monte_carlo.py for classical baseline.',
        'Open L2B_01_stamatopoulos_options_2020 for JPMorgan implementation view.',
        ]
    )


if __name__ == "__main__":
    main()
