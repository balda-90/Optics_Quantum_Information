# 04 — Quantum electronics

Light-matter interaction, two-level systems, lasers: the physics used to
actually build and control qubits. Prefer **notebooks** for theory + plots.

## Log

| Date       | File                                       | What I did |
|------------|--------------------------------------------|------------|
| 2026-07-04 | `01_rabi_oscillations.ipynb`               | Integrated the Schrodinger equation of a driven two-level system; Rabi oscillations on and off resonance. (Converted from `.py` on 2026-08-02.) |
| 2026-07-19 | `02_semiconductor_states_and_dos.ipynb`     | Guided notebook from semiconductor lasers to the density of states, Fermi–Dirac, 2D quantum wells and energy paraboloids. |
| 2026-10-11 | `03_course_recap.ipynb`                    | Public recap of the whole course after the May–September 2026 lectures: Rabi, rate equations, semiconductor inversion, 1D photonic bands, SPP dispersion, quantum-dot spectrum. (Converted from `.py`.) |
| 2026-11-01 | `04_cavity_qswitch_modelock.ipynb`         | Fabry–Pérot Airy / finesse, photon lifetime and Q, Q-switch pulse, mode-locked vs random-phase multimode train. |
| 2026-11-01 | `05_lindblad_t1_t2.ipynb`                  | Lindblad master equation: unitary Rabi check, $T_1$ envelope, extra dephasing $T_2<2T_1$. |

## Next steps
- Pi and pi/2 pulses as gates (X and sqrt(X)) with finite $T_2$: fidelity vs pulse length.
- Absorption spectrum: Fourier of the coherence = Lorentzian of width $1/T_2$.
- Turn the recap rate-equation demo into a pump–output (L–I) curve.
