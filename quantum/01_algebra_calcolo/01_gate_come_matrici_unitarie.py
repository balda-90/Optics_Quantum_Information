"""
Materia: 1 - Fondamenti di algebra e calcolo matematico
Tema del giorno: i gate quantistici SONO matrici unitarie.

Idea: tutta l'algebra lineare che studi (matrici, autovalori, prodotto
tensoriale) è esattamente il linguaggio con cui si descrivono i qubit.
Qui verifichiamo "a mano", con numpy, alcune proprieta' fondamentali.

Esecuzione:
    python quantum/01_algebra_calcolo/01_gate_come_matrici_unitarie.py
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
    print("\n[1] I gate a 1 qubit sono unitari (U U^dagger = I)?")
    for name, gate in {"X": PAULI_X, "Y": PAULI_Y, "Z": PAULI_Z, "H": HADAMARD}.items():
        print(f"    {name}: {is_unitary(gate)}")


def check_eigenvalues() -> None:
    print("\n[2] Autovalori dei gate di Pauli (devono avere modulo 1):")
    for name, gate in {"X": PAULI_X, "Y": PAULI_Y, "Z": PAULI_Z}.items():
        eigvals = np.linalg.eigvals(gate)
        moduli = np.abs(eigvals)
        print(f"    {name}: autovalori={np.round(eigvals, 3)}  |lambda|={np.round(moduli, 3)}")


def tensor_product_demo() -> None:
    print("\n[3] Prodotto tensoriale: da 1 qubit a 2 qubit.")
    # Stato |0> tensore |1>  ==  |01>
    state_01 = np.kron(ket0, ket1)
    print(f"    |0> (x) |1> = |01> ->\n{state_01.real.astype(int).flatten()}")

    # Gate H sul primo qubit, identita' sul secondo: H (x) I  (matrice 4x4)
    H_otimes_I = np.kron(HADAMARD, np.eye(2))
    print(f"    dim(H (x) I) = {H_otimes_I.shape}  unitaria? {is_unitary(H_otimes_I)}")


def superposition_demo() -> None:
    print("\n[4] Sovrapposizione: H|0> = (|0> + |1>)/sqrt(2).")
    psi = HADAMARD @ ket0
    probs = np.abs(psi.flatten()) ** 2
    print(f"    Ampiezze = {np.round(psi.flatten(), 3)}")
    print(f"    Probabilita' [P(0), P(1)] = {np.round(probs, 3)}")


def main() -> None:
    banner("Algebra lineare -> Quantum gates")
    check_unitarity()
    check_eigenvalues()
    tensor_product_demo()
    superposition_demo()
    print("\nFatto. Prossimo passo suggerito: dimostrare che X, Y, Z anticommutano.")


if __name__ == "__main__":
    main()
