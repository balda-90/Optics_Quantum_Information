# 03 — Introduction to Quantum Mechanics

From the postulates (state, evolution, measurement) to the phenomena with no
classical analogue: superposition and entanglement. Prefer **notebooks** for
theory + visualization.

## Log

| Date       | File                                       | What I did |
|------------|--------------------------------------------|------------|
| 2026-07-04 | `01_bell_state_entanglement.ipynb`         | Built the Bell state \|Phi+> with H + CNOT (Qiskit + Aer, NumPy fallback); measured correlations (00/11 ~100%). (Converted from `.py` on 2026-08-02.) |
| 2026-08-01 | `02_bra_ket_operators_eigenfunctions.ipynb` | Didactic notebook: Dirac bra–ket, operators, spectral theorem, wave functions as ⟨x\|ψ⟩, infinite-well eigenfunctions, wave-packet expansion. |

## Next steps
- Time evolution of the wave packet: $\psi(x,t)=\sum_n c_n\psi_n(x)e^{-iE_n t/\hbar}$.
- Bell's inequality / CHSH test: violate the classical bound of 2.
- The 4 Bell states and how to distinguish them.
- Quantum teleportation with 3 qubits.

> Run with Qiskit 2.x + qiskit-aer in `.venv-quantum` for the Bell notebook;
> the bra–ket notebook only needs numpy/matplotlib.
