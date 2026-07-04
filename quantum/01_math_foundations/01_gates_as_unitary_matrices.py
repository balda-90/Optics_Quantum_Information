"""
Subject: 1 - Mathematical foundations (algebra & calculus)
Topic of the day: quantum gates ARE unitary matrices.

Idea: all the linear algebra you study (matrices, eigenvalues, tensor
products) is exactly the language used to describe qubits. Here we verify
"by hand", with numpy, some of the fundamental properties.

Run:
    python quantum/01_math_foundations/01_gates_as_unitary_matrices.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from _common import (
    PAULI_X,
    PAULI_Y,
    PAULI_Z,
    HADAMARD,
    ket0,
    ket1,
    is_unitary,
    banner,
)


def check_unitarity() -> None:
    print("\n[1] Are the 1-qubit gates unitary (U U^dagger = I)?")
    for name, gate in {"X": PAULI_X, "Y": PAULI_Y, "Z": PAULI_Z, "H": HADAMARD}.items():
        print(f"    {name}: {is_unitary(gate)}")


def check_eigenvalues() -> None:
    print("\n[2] Eigenvalues of the Pauli gates (must have modulus 1):")
    for name, gate in {"X": PAULI_X, "Y": PAULI_Y, "Z": PAULI_Z}.items():
        eigvals = np.linalg.eigvals(gate)
        moduli = np.abs(eigvals)
        print(f"    {name}: eigenvalues={np.round(eigvals, 3)}  |lambda|={np.round(moduli, 3)}")


def tensor_product_demo() -> None:
    print("\n[3] Tensor product: from 1 qubit to 2 qubits.")
    # State |0> tensor |1>  ==  |01>
    state_01 = np.kron(ket0, ket1)
    print(f"    |0> (x) |1> = |01> ->\n{state_01.real.astype(int).flatten()}")

    # H on the first qubit, identity on the second: H (x) I  (4x4 matrix)
    H_otimes_I = np.kron(HADAMARD, np.eye(2))
    print(f"    dim(H (x) I) = {H_otimes_I.shape}  unitary? {is_unitary(H_otimes_I)}")


def superposition_demo() -> None:
    print("\n[4] Superposition: H|0> = (|0> + |1>)/sqrt(2).")
    psi = HADAMARD @ ket0
    probs = np.abs(psi.flatten()) ** 2
    print(f"    Amplitudes = {np.round(psi.flatten(), 3)}")
    print(f"    Probabilities [P(0), P(1)] = {np.round(probs, 3)}")


def main() -> None:
    banner("Linear algebra -> Quantum gates")
    check_unitarity()
    check_eigenvalues()
    tensor_product_demo()
    superposition_demo()
    print("\nDone. Suggested next step: prove that X, Y, Z anticommute.")


if __name__ == "__main__":
    main()
