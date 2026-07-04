"""
Materia: 2 - Ottica
Tema del giorno: la polarizzazione della luce e' un qubit.

Idea: uno stato di polarizzazione (orizzontale |H>, verticale |V>) si mappa
esattamente sulla base computazionale (|0>, |1>) di un qubit. La legge di
Malus per i polarizzatori diventa la regola di misura di Born.

Esecuzione:
    python quantum/02_ottica/01_polarizzazione_come_qubit.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import matplotlib

matplotlib.use("Agg")  # backend senza finestra: salva su file
import matplotlib.pyplot as plt

from _common import ket0, ket1, savefig, banner


def polarization_state(theta_deg: float) -> np.ndarray:
    """Stato di polarizzazione lineare a un angolo theta rispetto all'orizzontale."""
    theta = np.deg2rad(theta_deg)
    return np.cos(theta) * ket0 + np.sin(theta) * ket1


def malus_from_born(theta_deg: float) -> float:
    """
    Probabilita' che un fotone polarizzato a theta passi un polarizzatore
    orizzontale. Regola di Born: P = |<H|psi>|^2 = cos^2(theta) = legge di Malus.
    """
    psi = polarization_state(theta_deg)
    amp_H = (ket0.conj().T @ psi).item()
    return float(abs(amp_H) ** 2)


def demo_numeric() -> None:
    print("\n[1] Legge di Malus come regola di Born (P = cos^2 theta):")
    for theta in (0, 30, 45, 60, 90):
        p = malus_from_born(theta)
        print(f"    theta={theta:>3} gradi -> P(passa) = {p:.3f}  (cos^2 = {np.cos(np.deg2rad(theta))**2:.3f})")


def demo_plot() -> None:
    thetas = np.linspace(0, 180, 361)
    probs = [malus_from_born(t) for t in thetas]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(thetas, probs, label=r"$P=\cos^2\theta$ (Born / Malus)")
    ax.set_xlabel("Angolo di polarizzazione theta [gradi]")
    ax.set_ylabel("Probabilita' di trasmissione")
    ax.set_title("Ottica -> Qubit: polarizzazione e legge di Malus")
    ax.grid(True, alpha=0.3)
    ax.legend()
    path = savefig(fig, __file__, "malus_born.png")
    plt.close(fig)
    print(f"\n[2] Grafico salvato in: {path}")


def main() -> None:
    banner("Ottica -> Polarizzazione come qubit")
    demo_numeric()
    demo_plot()
    print("\nFatto. Prossimo passo: modellare un beam splitter come gate di Hadamard.")


if __name__ == "__main__":
    main()
