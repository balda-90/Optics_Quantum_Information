"""
Utility condivise per i mini-progetti di quantum computing del master.

Volutamente leggere: dipendono solo da numpy (e matplotlib per i grafici),
così ogni script per materia può importarle senza trascinare l'intero stack.
Gli import "pesanti" (qiskit, ecc.) restano dentro i singoli script.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime

import numpy as np

# --- Stati di base (base computazionale) ---
ket0 = np.array([[1], [0]], dtype=complex)
ket1 = np.array([[0], [1]], dtype=complex)

# --- Matrici di Pauli e Hadamard ---
PAULI_I = np.array([[1, 0], [0, 1]], dtype=complex)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)
HADAMARD = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)


def is_unitary(matrix: np.ndarray, tol: float = 1e-10) -> bool:
    """True se la matrice è unitaria (U U^dagger = I) entro tolleranza."""
    matrix = np.asarray(matrix, dtype=complex)
    n = matrix.shape[0]
    return np.allclose(matrix @ matrix.conj().T, np.eye(n), atol=tol)


def bloch_coordinates(state: np.ndarray) -> tuple[float, float, float]:
    """
    Converte uno stato puro di 1 qubit (vettore 2x1 o 1D di lunghezza 2)
    nelle coordinate (x, y, z) sulla sfera di Bloch.
    """
    psi = np.asarray(state, dtype=complex).reshape(2)
    psi = psi / np.linalg.norm(psi)
    a, b = psi[0], psi[1]
    x = 2 * (a.conjugate() * b).real
    y = 2 * (a.conjugate() * b).imag
    z = (abs(a) ** 2 - abs(b) ** 2).real
    return float(x), float(y), float(z)


def output_dir(script_file: str) -> Path:
    """
    Restituisce (creandola) una cartella 'output' accanto allo script chiamante.
    Uso tipico: output_dir(__file__).
    """
    d = Path(script_file).resolve().parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def savefig(fig, script_file: str, name: str) -> Path:
    """Salva una figura matplotlib nella cartella output/ della materia."""
    out = output_dir(script_file) / name
    fig.savefig(out, dpi=150, bbox_inches="tight")
    return out


def banner(title: str) -> None:
    """Stampa un'intestazione leggibile con timestamp, utile nei log giornalieri."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = "=" * max(60, len(title) + 4)
    print(line)
    print(f"  {title}")
    print(f"  [{stamp}]")
    print(line)
