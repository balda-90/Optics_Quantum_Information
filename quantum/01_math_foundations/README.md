# 01 — Mathematical foundations (algebra & calculus)

The bridge between this subject and quantum computing is direct: **states =
vectors**, **gates = unitary matrices**, **measurements = projections**. Here I
build the algebraic intuition needed for everything else.

Prefer **Jupyter notebooks** for theory + runnable checks.

## Log

| Date       | File                                      | What I did |
|------------|-------------------------------------------|------------|
| 2026-07-04 | `01_gates_as_unitary_matrices.ipynb`      | Verified unitarity of the gates (X, Y, Z, H), Pauli eigenvalues, tensor product, and superposition with Hadamard. (Converted from `.py` on 2026-08-02.) |
| 2026-11-01 | `02_frobenius_perturbation.ipynb`         | Power series for $y''+y=0$; Frobenius $J_0$; secular terms of naive perturbation on the weakly damped oscillator. |

## Next steps
- Poincaré–Lindstedt: stretch time $\tau=\omega(\varepsilon)t$ and kill secular terms order by order.
- Hermite as a second Frobenius example (quantum harmonic oscillator).
- Numerically prove that X, Y, Z anticommute ({X,Y}=0, etc.).

## Related notebook
For a full bra–ket → wave-function → eigenfunction path, see
`../03_quantum_mechanics/02_bra_ket_operators_eigenfunctions.ipynb`.
