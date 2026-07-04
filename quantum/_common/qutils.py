"""
Shared utilities for the master's quantum-computing mini-projects.

Deliberately lightweight: they depend only on numpy (and matplotlib for plots),
so every per-subject script can import them without pulling in the whole stack.
The "heavy" imports (qiskit, etc.) stay inside the individual scripts.
"""
from __future__ import annotations

from pathlib import Path
from datetime import datetime

import numpy as np

# --- Basis states (computational basis) ---
ket0 = np.array([[1], [0]], dtype=complex)
ket1 = np.array([[0], [1]], dtype=complex)

# --- Pauli matrices and Hadamard ---
PAULI_I = np.array([[1, 0], [0, 1]], dtype=complex)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)
HADAMARD = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)


def is_unitary(matrix: np.ndarray, tol: float = 1e-10) -> bool:
    """Return True if the matrix is unitary (U U^dagger = I) within tolerance."""
    matrix = np.asarray(matrix, dtype=complex)
    n = matrix.shape[0]
    return np.allclose(matrix @ matrix.conj().T, np.eye(n), atol=tol)


def bloch_coordinates(state: np.ndarray) -> tuple[float, float, float]:
    """
    Convert a pure 1-qubit state (2x1 vector or 1D array of length 2)
    into its (x, y, z) coordinates on the Bloch sphere.
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
    Return (creating it if needed) an 'output' folder next to the calling script.
    Typical use: output_dir(__file__).
    """
    d = Path(script_file).resolve().parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def savefig(fig, script_file: str, name: str) -> Path:
    """Save a matplotlib figure into the subject's output/ folder."""
    out = output_dir(script_file) / name
    fig.savefig(out, dpi=150, bbox_inches="tight")
    return out


def banner(title: str) -> None:
    """Print a readable header with a timestamp, handy for the daily logs."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = "=" * max(60, len(title) + 4)
    print(line)
    print(f"  {title}")
    print(f"  [{stamp}]")
    print(line)
