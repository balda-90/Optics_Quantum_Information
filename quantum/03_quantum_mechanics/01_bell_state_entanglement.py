"""
Subject: 3 - Introduction to Quantum Mechanics
Topic of the day: entanglement and the Bell state.

Idea: we build the Bell state |Phi+> = (|00> + |11>)/sqrt(2) with an
H + CNOT circuit and measure the correlations. We see that the two qubits,
while individually random, ALWAYS yield equal outcomes: that is entanglement.

If qiskit is installed it uses the Aer simulator; otherwise it does the same
computation with numpy, so the script runs regardless.

Run:
    python quantum/03_quantum_mechanics/01_bell_state_entanglement.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# The Windows console often uses cp1252, which cannot render the box-drawing
# characters of Qiskit circuit diagrams. Force UTF-8 on output when possible.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

import numpy as np

from _common import ket0, HADAMARD, banner


def bell_with_numpy(shots: int = 1000) -> dict[str, int]:
    """Build |Phi+> with linear algebra and sample the measurements."""
    # |00>
    state = np.kron(ket0, ket0)
    # H on the first qubit
    H_I = np.kron(HADAMARD, np.eye(2))
    state = H_I @ state
    # CNOT (control = qubit 0, target = qubit 1)
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
    """True if qiskit and qiskit-aer can be imported."""
    try:
        import qiskit  # noqa: F401
        import qiskit_aer  # noqa: F401
        return True
    except ImportError:
        return False


def bell_with_qiskit(shots: int = 1000):
    """Same Bell state, but with a real Qiskit circuit + Aer."""
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
    Draw the circuit. On Windows the box drawing may fail due to the console
    encoding: in that case fall back to a pure-ASCII rendering.
    """
    try:
        print(qc.draw(output="text"))
    except UnicodeEncodeError:
        drawing = qc.draw(output="text")
        print(str(drawing).encode("ascii", "replace").decode("ascii"))


def main() -> None:
    banner("Quantum mechanics -> Bell state")
    shots = 1000

    if qiskit_available():
        counts, qc = bell_with_qiskit(shots)
        print("\n[Qiskit] Circuit:")
        draw_circuit(qc)
        engine = "Qiskit + Aer"
    else:
        print("\n[Info] Qiskit not installed, using numpy. Install with: pip install qiskit qiskit-aer")
        counts = bell_with_numpy(shots)
        engine = "numpy"

    print(f"\n[{engine}] Counts over {shots} measurements:")
    for label, n in counts.items():
        print(f"    |{label}>: {n:>4}  ({100 * n / shots:.1f}%)")

    same = counts.get("00", 0) + counts.get("11", 0)
    print(f"\nCorrelated outcomes (00 or 11): {100 * same / shots:.1f}%  -> expected ~100% for |Phi+>.")
    print("\nDone. Next step: check Bell's inequality (CHSH).")


if __name__ == "__main__":
    main()
