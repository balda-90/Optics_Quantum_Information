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

# La console di Windows usa spesso cp1252, che non gestisce i caratteri del
# disegno dei circuiti Qiskit. Forziamo UTF-8 sull'output quando possibile.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

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


def qiskit_available() -> bool:
    """True se qiskit e qiskit-aer sono importabili."""
    try:
        import qiskit  # noqa: F401
        import qiskit_aer  # noqa: F401
        return True
    except ImportError:
        return False


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


def draw_circuit(qc) -> None:
    """
    Disegna il circuito. Su Windows il disegno a box puo' fallire per l'encoding
    della console: in quel caso ripiega su un disegno in caratteri ASCII.
    """
    try:
        print(qc.draw(output="text"))
    except UnicodeEncodeError:
        drawing = qc.draw(output="text")
        print(str(drawing).encode("ascii", "replace").decode("ascii"))


def main() -> None:
    banner("Meccanica quantistica -> Stato di Bell")
    shots = 1000

    if qiskit_available():
        counts, qc = bell_with_qiskit(shots)
        print("\n[Qiskit] Circuito:")
        draw_circuit(qc)
        engine = "Qiskit + Aer"
    else:
        print("\n[Info] Qiskit non installato, uso numpy. Installa con: pip install qiskit qiskit-aer")
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
