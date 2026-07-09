"""
Tutorial — Pricing Options on Quantum Computers — Jauron (Sherbrooke) 2022
Slug: L3_01_jauron_thesis_2022
Level: L3 — Reference theses

Run from repo root:
    python quantum/tesi/papers/L3_thesis_ref/L3_01_jauron_thesis_2022.py
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
    """Thesis-style checklist metrics for a European call run."""
    S0, K, r, sigma, T = 100, 105, 0.03, 0.25, 0.5
    d1 = (np.log(S0/K) + (r+0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    bs = S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    steps = ["Define payoff", "Build oracle", "Run QAE", "Compare to BS"]
    explain("Workflow steps with final Black-Scholes reference.")
    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")
    print(f"\n  Black-Scholes call price = {bs:.4f}")
    print(f"  Target MC stderr ~ 0.01 needs ~{(1.96/0.01)**2 * 0.25:.0f} paths (rough)")


def main() -> None:
    banner('Pricing Options on Quantum Computers — Jauron (Sherbrooke) 2022', "Master's thesis — pricing options on quantum computers")
    paper_info(
        'Pricing Options on Quantum Computers — Jauron (Sherbrooke) 2022',
        "Master's thesis: full option pricing workflow on QC.",
        arxiv='',
        level='L3 — Reference theses',
    )

    section(1, "The Finance Problem")
    explain(
        'Thesis work needs a reproducible pipeline from payoff definition to quantum circuit metrics and error analysis.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Jauron (Sherbrooke, 2022) implements European option pricing with QAE, documenting circuits, simulations, and hardware considerations.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Thesis workflow', 'Problem -> classical baseline -> quantum design -> evaluation.'),
        ('Circuit depth', 'Gate count layers affecting noise sensitivity.'),
        ('Simulation vs hardware', 'Ideal simulators vs noisy device results.'),
        ]
    )
    analogy('A thesis is a lab notebook with receipts—every claim tied to a script, circuit, or plot.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Thesis instances are smaller than production books.',
        'Hardware results age as devices improve.',
        'Some steps rely on simulators only.',
    )

    section(6, "Recap")
    recap(
        [
        'Jauron is a reference implementation narrative.',
        'Always anchor to classical MC/BS prices.',
        'Document depth, shots, and error bars.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read Berube 2024 thesis for improvements.',
        'Run quantum/tesi/02_european_option_monte_carlo.py.',
        'Reproduce payoff oracle on paper for 1-qubit toy.',
        ]
    )


if __name__ == "__main__":
    main()
