# 03 — Introduction to Quantum Mechanics

From the postulates (state, evolution, measurement) to the phenomena with no
classical analogue: superposition and entanglement. Prefer **notebooks** for
theory + visualization; keep short `.py` scripts when a circuit demo is enough.

## Log

| Date       | File                                      | What I did |
|------------|-------------------------------------------|------------|
| 2026-07-04 | `01_bell_state_entanglement.py`           | Built the Bell state \|Phi+> with H + CNOT on a Qiskit circuit + Aer simulator; drew the circuit and measured the correlations (00/11 ~100%). Numpy fallback if Qiskit is missing. |
| 2026-08-01 | `02_bra_ket_operators_eigenfunctions.ipynb` | Didactic notebook: Dirac bra–ket, inner products, Hermitian/unitary operators, spectral theorem, expectation values; wave functions as ⟨x\|ψ⟩; infinite-well eigenfunctions/eigenvalues (analytic + finite-difference); expanding a wave packet in the energy basis. |

## Next steps
- Time evolution of the wave packet: $\psi(x,t)=\sum_n c_n\psi_n(x)e^{-iE_n t/\hbar}$.
- Bell's inequality / CHSH test: violate the classical bound of 2.
- The 4 Bell states and how to distinguish them.
- Quantum teleportation with 3 qubits.

> Run with Qiskit 2.x + qiskit-aer in the dedicated `.venv-quantum` environment
> (needed for `01_...`; the bra–ket notebook only needs numpy/matplotlib).
