"""
Materia: 4 - Elettronica quantistica
Tema del giorno: oscillazioni di Rabi di un sistema a due livelli.

Idea: un atomo a due livelli (o un qubit) guidato da un campo risonante
oscilla tra stato fondamentale ed eccitato: sono le oscillazioni di Rabi,
il cuore dell'interazione luce-materia e dei laser. Integriamo l'equazione
di Schrodinger e disegniamo la popolazione dell'eccitato nel tempo.

Esecuzione:
    python quantum/04_elettronica_quantistica/01_oscillazioni_di_rabi.py
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
    omega_rabi: float = 2 * np.pi * 1.0,   # frequenza di Rabi [rad/s]
    detuning: float = 0.0,                 # disaccordo dalla risonanza [rad/s]
    t_max: float = 2.0,
    n_steps: int = 2000,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Integra la Schrodinger per un due-livelli:
        H = (detuning/2) Z + (omega_rabi/2) X
    Ritorna (tempi, popolazione dello stato eccitato |1>).
    """
    H = 0.5 * detuning * PAULI_Z + 0.5 * omega_rabi * PAULI_X
    times = np.linspace(0.0, t_max, n_steps)
    dt = times[1] - times[0]

    # Propagatore per passo: U = exp(-i H dt), qui via diagonalizzazione
    eigvals, eigvecs = np.linalg.eigh(H)
    U = eigvecs @ np.diag(np.exp(-1j * eigvals * dt)) @ eigvecs.conj().T

    psi = ket0.astype(complex).copy()
    pop_excited = np.empty(n_steps)
    for k in range(n_steps):
        pop_excited[k] = abs(psi[1, 0]) ** 2
        psi = U @ psi
    return times, pop_excited


def main() -> None:
    banner("Elettronica quantistica -> Oscillazioni di Rabi")

    fig, ax = plt.subplots(figsize=(7, 4))
    for detuning, label in [(0.0, "risonante (detuning=0)"),
                            (2 * np.pi * 1.0, "fuori risonanza")]:
        t, pop = simulate_rabi(detuning=detuning)
        ax.plot(t, pop, label=label)
        print(f"    {label}: popolazione max eccitato = {pop.max():.3f}")

    ax.set_xlabel("Tempo [s]")
    ax.set_ylabel("Popolazione stato eccitato |1>")
    ax.set_title("Oscillazioni di Rabi in un sistema a due livelli")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    from _common import savefig
    path = savefig(fig, __file__, "rabi_oscillations.png")
    plt.close(fig)
    print(f"\nGrafico salvato in: {path}")
    print("\nFatto. Prossimo passo: aggiungere il decadimento (equazione di Lindblad).")


if __name__ == "__main__":
    main()
