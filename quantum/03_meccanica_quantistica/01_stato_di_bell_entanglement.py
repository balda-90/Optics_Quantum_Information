"""
Materia: 3 - Introduzione alla Meccanica Quantistica
Tema del giorno: entanglement e stato di Bell.

Idea: costruiamo lo stato di Bell |Phi+> = (|00> + |11>)/sqrt(2) con un
circuito H + CNOT e misuriamo le correlazioni. Vediamo che i due qubit,
pur essendo casuali singolarmente, danno SEMPRE esiti uguali: e' entanglement.

Se qiskit e' installato usa il simulatore Aer; altrimenti fa lo stesso conto
con numpy, cosi' lo script gira comunque.

Esecuzione:
    python quantum/03_meccanica_quantistica/01_stato_di_bell_entanglement.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from _common import ket0, HADAMARD, banner


def bell_with_numpy(shots: int = 1000) -> dict[str, int]:
    """Costruisce |Phi+> con algebra lineare e campiona le misure."""
    # |00>
    state = np.kron(ket0, ket0)
    # H sul primo qubit
    H_I = np.kron(HADAMARD, np.eye(2))
    state = H_I @ state
    # CNOT (controllo = qubit 0, target = qubit 1)
    cnot = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 1],
         [0, 0, 1, 0]],
        dtype=complex,
    )
    state = cnot @ state

    probs = np.abs(state.flatten()) ** 2
    labels = ["00", "01", "10", "11"]
    outcomes = np.random.choice(labels, size=shots, p=probs)
    counts: dict[str, int] = {}
    for o in outcomes:
        counts[o] = counts.get(o, 0) + 1
    return dict(sorted(counts.items()))


def bell_with_qiskit(shots: int = 1000):
    """Stesso stato di Bell, ma con un vero circuito Qiskit + Aer."""
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    sim = AerSimulator()
    result = sim.run(qc, shots=shots).result()
    return dict(sorted(result.get_counts().items())), qc


def main() -> None:
    banner("Meccanica quantistica -> Stato di Bell")
    shots = 1000

    try:
        counts, qc = bell_with_qiskit(shots)
        print("\n[Qiskit] Circuito:")
        print(qc.draw(output="text"))
        engine = "Qiskit + Aer"
    except Exception as exc:  # qiskit non installato o errore backend
        print(f"\n[Info] Qiskit non disponibile ({type(exc).__name__}), uso numpy.")
        counts = bell_with_numpy(shots)
        engine = "numpy"

    print(f"\n[{engine}] Conteggi su {shots} misure:")
    for label, n in counts.items():
        print(f"    |{label}>: {n:>4}  ({100 * n / shots:.1f}%)")

    same = counts.get("00", 0) + counts.get("11", 0)
    print(f"\nEsiti correlati (00 o 11): {100 * same / shots:.1f}%  -> atteso ~100% per |Phi+>.")
    print("\nFatto. Prossimo passo: verificare la disuguaglianza di Bell (CHSH).")


if __name__ == "__main__":
    main()
