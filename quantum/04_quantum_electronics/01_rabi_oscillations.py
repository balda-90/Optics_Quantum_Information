"""
Subject: 4 - Quantum electronics
Topic of the day: Rabi oscillations of a two-level system.

Idea: a two-level atom (or a qubit) driven by a resonant field oscillates
between ground and excited state: these are Rabi oscillations, the heart of
light-matter interaction and of lasers. We integrate the Schrodinger equation
and plot the excited-state population over time.

Run:
    python quantum/04_quantum_electronics/01_rabi_oscillations.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import ket0, PAULI_X, PAULI_Z, banner


def simulate_rabi(
    omega_rabi: float = 2 * np.pi * 1.0,   # Rabi frequency [rad/s]
    detuning: float = 0.0,                 # detuning from resonance [rad/s]
    t_max: float = 2.0,
    n_steps: int = 2000,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Integrate the Schrodinger equation for a two-level system:
        H = (detuning/2) Z + (omega_rabi/2) X
    Returns (times, excited-state |1> population).
    """
    H = 0.5 * detuning * PAULI_Z + 0.5 * omega_rabi * PAULI_X
    times = np.linspace(0.0, t_max, n_steps)
    dt = times[1] - times[0]

    # Per-step propagator: U = exp(-i H dt), here via diagonalization
    eigvals, eigvecs = np.linalg.eigh(H)
    U = eigvecs @ np.diag(np.exp(-1j * eigvals * dt)) @ eigvecs.conj().T

    psi = ket0.astype(complex).copy()
    pop_excited = np.empty(n_steps)
    for k in range(n_steps):
        pop_excited[k] = abs(psi[1, 0]) ** 2
        psi = U @ psi
    return times, pop_excited


def main() -> None:
    banner("Quantum electronics -> Rabi oscillations")

    fig, ax = plt.subplots(figsize=(7, 4))
    for detuning, label in [(0.0, "resonant (detuning=0)"),
                            (2 * np.pi * 1.0, "off-resonance")]:
        t, pop = simulate_rabi(detuning=detuning)
        ax.plot(t, pop, label=label)
        print(f"    {label}: max excited-state population = {pop.max():.3f}")

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Excited-state population |1>")
    ax.set_title("Rabi oscillations in a two-level system")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    from _common import savefig
    path = savefig(fig, __file__, "rabi_oscillations.png")
    plt.close(fig)
    print(f"\nPlot saved to: {path}")
    print("\nDone. Next step: add decay (Lindblad master equation).")


if __name__ == "__main__":
    main()
