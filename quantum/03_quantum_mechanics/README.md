# 03 — Introduction to Quantum Mechanics

From the postulates (state, evolution, measurement) to the phenomena with no
classical analogue: superposition and entanglement. Here I touch them via
circuits.

## Log

| Date       | Script                            | What I did |
|------------|-----------------------------------|------------|
| 2026-07-04 | `01_bell_state_entanglement.py`   | Built the Bell state |Phi+> with H + CNOT on a Qiskit circuit + Aer simulator; drew the circuit and measured the correlations (00/11 ~100%). Numpy fallback if Qiskit is missing. |

## Next steps
- Bell's inequality / CHSH test: violate the classical bound of 2.
- The 4 Bell states and how to distinguish them.
- Quantum teleportation with 3 qubits.

> Run with Qiskit 2.x + qiskit-aer in the dedicated `.venv-quantum` environment.
