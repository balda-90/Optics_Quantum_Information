"""
Tutorial — Quantum Computing for Finance — Egger et al. (IBM) 2020
Slug: L0_02_egger_2020
Level: L0 — Foundations

Run from repo root:
    python quantum/tesi/papers/L0_fondamenta/L0_02_egger_2020.py
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
    """Maturity score vs required qubits for three finance workloads."""
    workloads = ["Portfolio VQE", "Option QAE", "Fraud QML"]
    maturity = np.array([0.55, 0.40, 0.30])
    qubits_needed = np.array([80, 200, 120])
    explain(
        "We plot illustrative maturity (0–1) against estimated qubit needs.",
        "Higher maturity means closer to industry pilot; qubits are rough order-of-magnitude.",
    )
    for w, m, q in zip(workloads, maturity, qubits_needed):
        print(f"  {w:16s} | maturity={m:.2f} | est. qubits={q}")
    # Sigmoid readiness curve vs year
    years = np.linspace(2020, 2030, 50)
    readiness = 1 / (1 + np.exp(-(years - 2027) / 1.2))
    print(f"\n  Projected industry readiness in 2026: {readiness[years >= 2026][0]:.2f}")


def main() -> None:
    banner('Quantum Computing for Finance — Egger et al. (IBM) 2020', 'IBM state-of-the-art and near-term finance roadmap')
    paper_info(
        'Quantum Computing for Finance — Egger et al. (IBM) 2020',
        'State-of-the-art and roadmap for near-term finance applications.',
        arxiv='2006.14510',
        level='L0 — Foundations',
    )

    section(1, "The Finance Problem")
    explain(
        'Financial institutions need a realistic timeline: when can quantum computing help with production workloads, not just toy models?',
        'Egger et al. (2020) evaluate algorithms against near-term hardware constraints and classical baselines.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'The authors update the finance quantum landscape with emphasis on variational algorithms, annealing, and amplitude estimation pipelines.',
        'They discuss what is feasible on NISQ devices versus what needs error-corrected machines.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('NISQ', 'Noisy Intermediate-Scale Quantum: devices with tens–hundreds of qubits and imperfect gates.'),
        ('Variational quantum algorithm', 'A hybrid loop where a classical optimizer tunes quantum circuit parameters.'),
        ('Resource estimation', 'Counting qubits, circuit depth, and shots needed to beat a classical method.'),
        ]
    )
    analogy("Egger's roadmap is like a product release plan: some features ship in beta (NISQ pilots), others need the next major platform (fault tolerance).")

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Roadmaps age quickly as hardware and classical algorithms improve.',
        'Pilot success on synthetic data may not transfer to messy production datasets.',
        'Integration with existing risk systems is non-trivial.',
    )

    section(6, "Recap")
    recap(
        [
        'Egger 2020 bridges theory and near-term engineering reality.',
        'Finance use cases must be judged with resource budgets.',
        'Hybrid classical-quantum workflows are the practical default.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Compare with Orus 2019 to see how priorities shifted.',
        'Explore VQE portfolio demo in L2A_02_bbva_vqe_2025 tutorial.',
        'Read Goldman 2022 for risk-specific resource estimates.',
        ]
    )


if __name__ == "__main__":
    main()
