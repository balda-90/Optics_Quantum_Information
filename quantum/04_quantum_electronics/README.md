# 04 — Quantum electronics

Light-matter interaction, two-level systems, lasers: the physics used to
actually build and control qubits. Here I simulate the dynamics.

## Log

| Date       | Script                      | What I did |
|------------|-----------------------------|------------|
| 2026-07-04 | `01_rabi_oscillations.py`   | Integrated the Schrodinger equation of a driven two-level system; Rabi oscillations on and off resonance; plotted the population. |
| 2026-07-19 | `02_semiconductor_states_and_dos.ipynb` | Guided notebook from semiconductor lasers to the density of states: free electrons and the E(k) parabola, Schrodinger for V=0, the potential well and discrete levels, k-space and spherical state counting, 3D DOS, Fermi-Dirac and the Fermi level, occupied states g(E)f(E) at T>0, quantum-well subbands E_n + hbar^2 k^2/2m, staircase DOS and 3D energy paraboloids. |

## Next steps
- Add decay (Lindblad master equation, T1/T2).
- Pi and pi/2 pulses as gates (X and sqrt(X)).
- Absorption spectrum and line broadening.
