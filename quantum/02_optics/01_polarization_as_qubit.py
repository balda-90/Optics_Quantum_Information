"""
Subject: 2 - Optics
Topic of the day: the polarization of light is a qubit.

Idea: a polarization state (horizontal |H>, vertical |V>) maps exactly onto
the computational basis (|0>, |1>) of a qubit. Malus's law for polarizers
becomes the Born measurement rule.

Run:
    python quantum/02_optics/01_polarization_as_qubit.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib

matplotlib.use("Agg")  # windowless backend: saves to file
import matplotlib.pyplot as plt

from _common import ket0, ket1, savefig, banner


def polarization_state(theta_deg: float) -> np.ndarray:
    """Linear polarization state at angle theta with respect to horizontal."""
    theta = np.deg2rad(theta_deg)
    return np.cos(theta) * ket0 + np.sin(theta) * ket1


def malus_from_born(theta_deg: float) -> float:
    """
    Probability that a photon polarized at theta passes a horizontal polarizer.
    Born rule: P = |<H|psi>|^2 = cos^2(theta) = Malus's law.
    """
    psi = polarization_state(theta_deg)
    amp_H = (ket0.conj().T @ psi).item()
    return float(abs(amp_H) ** 2)


def demo_numeric() -> None:
    print("\n[1] Malus's law as the Born rule (P = cos^2 theta):")
    for theta in (0, 30, 45, 60, 90):
        p = malus_from_born(theta)
        print(f"    theta={theta:>3} deg -> P(pass) = {p:.3f}  (cos^2 = {np.cos(np.deg2rad(theta))**2:.3f})")


def demo_plot() -> None:
    thetas = np.linspace(0, 180, 361)
    probs = [malus_from_born(t) for t in thetas]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(thetas, probs, label=r"$P=\cos^2\theta$ (Born / Malus)")
    ax.set_xlabel("Polarization angle theta [deg]")
    ax.set_ylabel("Transmission probability")
    ax.set_title("Optics -> Qubit: polarization and Malus's law")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path = savefig(fig, __file__, "malus_born.png")
    plt.close(fig)
    print(f"\n[2] Plot saved to: {path}")


def main() -> None:
    banner("Optics -> Polarization as a qubit")
    demo_numeric()
    demo_plot()
    print("\nDone. Next step: model a beam splitter as a Hadamard gate.")


if __name__ == "__main__":
    main()
