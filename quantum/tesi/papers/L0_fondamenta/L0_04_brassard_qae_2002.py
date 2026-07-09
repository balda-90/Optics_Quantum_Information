"""
Tutorial — Quantum Amplitude Estimation — Brassard et al. 2002
Slug: L0_04_brassard_qae_2002
Level: L0 — Foundations

Run from repo root:
    python quantum/tesi/papers/L0_fondamenta/L0_04_brassard_qae_2002.py
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
    """Simulate Grover-like amplitude amplification on a 1-qubit toy model."""
    theta = np.pi / 5  # initial amplitude a = sin(theta)
    a = np.sin(theta) ** 2
    explain(f"Target amplitude a = sin²(theta) = {a:.4f}")
    state = np.array([np.cos(theta), np.sin(theta)], dtype=complex)
    # Grover reflection about |0> and about psi
    def reflect_about_zero(psi):
        return np.array([psi[0], -psi[1]])
    def reflect_about_psi(psi, ref):
        proj = np.vdot(ref, psi) * ref
        return 2 * proj - psi
    amps = [a]
    psi = state.copy()
    for k in range(1, 6):
        psi = reflect_about_psi(reflect_about_zero(psi), state)
        psi = psi / np.linalg.norm(psi)
        amps.append(float(np.abs(psi[1]) ** 2))
    print("\n  Grover iterations -> amplified probability:")
    for k, p in enumerate(amps):
        print(f"    k={k}: P(target)={p:.4f}")


def main() -> None:
    banner('Quantum Amplitude Estimation — Brassard et al. 2002', 'Original Quantum Amplitude Estimation paper')
    paper_info(
        'Quantum Amplitude Estimation — Brassard et al. 2002',
        'Quadratic speedup for estimating amplitudes / probabilities.',
        arxiv='quant-ph/0005055',
        level='L0 — Foundations',
    )

    section(1, "The Finance Problem")
    explain(
        'Many finance metrics are probabilities or expectations: default events, positive payoff indicators, breach of VaR thresholds.',
        'Classical sampling needs many trials for high precision.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Brassard et al. (2002) introduce Quantum Amplitude Estimation and Quantum Amplitude Amplification (generalizing Grover search).',
        'Given a quantum state with amplitude a, QAE estimates a using O(1/ε) queries instead of O(1/ε²) classical samples.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Amplitude', 'The √probability component of a quantum state coefficient.'),
        ('Grover iterator', 'Repeated reflection operations that amplify target amplitudes.'),
        ('Phase estimation', 'Extracts eigenphases of unitary operators to read amplitudes.'),
        ]
    )
    analogy('Amplitude amplification is like turning up the volume on one instrument in an orchestra without replaying the whole concert many times.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Requires coherent quantum oracles and long circuits for high precision.',
        'Financial payoff oracles must be reversible and implementable.',
        'Error rates compound with depth on real devices.',
    )

    section(6, "Recap")
    recap(
        [
        'QAE is the theoretical engine behind many finance speedup claims.',
        'Amplification + phase estimation achieves 1/N-type scaling.',
        'Finance papers cite Brassard as the core reference.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Study Grover iterations in the demo below.',
        'Read Rebentrost MC 2018 for finance application.',
        'Try quantum/tesi/01_quantum_amplitude_estimation.py.',
        ]
    )


if __name__ == "__main__":
    main()
