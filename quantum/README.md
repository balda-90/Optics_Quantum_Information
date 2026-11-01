# Optics & Quantum Information — Coding Journal

Code developed during my master's in **Optics and Quantum Information**
(Sapienza University of Rome). The goal is to connect, subject by subject, the
course topics with **quantum computing** through small runnable scripts — one a
day — to build a public portfolio and my personal brand.

Repo: https://github.com/balda-90/Optics_Quantum_Information

## Master modules → this repo

Public **coding journal**, not an archive of lectures. Professor slides, Moodle
dumps and recordings stay in local `data/` and are gitignored.

| Master module | Folder here | Status |
|---|---|---|
| 4. Algebra and calculus (Carillo) | `01_math_foundations/` | gates as unitaries |
| 1. Optics (Bertolotti) | `02_optics/` | polarisation qubit, Maxwell / interfaces |
| 3. QM intro (Centini) | `03_quantum_mechanics/` | Bell, bra–ket, wells |
| 3. Laser & quantum electronics (Sibilia) | `04_quantum_electronics/` | Rabi, DOS, recap, cavity / pulses |
| 6. Quantum information I (Bovino) | `05_Basics of quantum information/` | circuits, teleportation, density matrices |
| 8. Thermal radiation & IR signature (Li Voti) | `06_radiazione_termica_segnatura_IR/` | conduction → IR signature |
| 2. Nonlinear optics (Wabnitz) | `07_nonlinear_optics/` | SHG, phase matching, $n_2$ |
| Thesis / quantum finance | `tesi/` | bibliography map + paper tutorials |

Modules not started yet (cryptography, QI II, quantum computing, devices,
optical transmission) will get a folder when the lectures begin.

## Structure

```
quantum/
├── _common/                # shared utilities (algebra, Bloch sphere, plotting)
├── 00_Paper_study/         # Paper-study / exploratory notebooks (AE, VaR, …)
├── 01_math_foundations/    # Mathematical foundations (algebra & calculus)
├── 02_optics/              # Optics
├── 03_quantum_mechanics/   # Introduction to Quantum Mechanics
├── 04_quantum_electronics/ # Quantum electronics
├── 05_Basics of quantum information/
├── 06_radiazione_termica_segnatura_IR/
├── 07_nonlinear_optics/    # χ² / χ³ recap
├── tesi/                   # Thesis: quantum finance bibliography & scripts
└── requirements.txt
```

Each subject folder contains numbered files (`01_...`, `02_...`) plus a
`README.md` that tracks what I learned/implemented each day. Prefer
**Jupyter notebooks** (`.ipynb`) when the topic mixes theory and plots; keep
short `.py` scripts for focused circuit / numerical demos.

## Setup

This code uses a **dedicated virtual environment** (`.venv-quantum`), separate
from the RAG assistant's `.venv`. Reason: Qiskit 2.x requires `numpy>=2.0`,
while the RAG stack (langchain) requires `numpy<2.0`. Keeping them separate
avoids conflicts.

```powershell
python -m venv .venv-quantum
.\.venv-quantum\Scripts\Activate.ps1
pip install -r quantum/requirements.txt
```

> Note: `numpy`, `scipy` and `matplotlib` are enough for most scripts.
> `qiskit` is only needed where indicated (e.g. real circuits and the Aer
> simulator). Scripts that can, fall back to numpy and run without qiskit.

## How to run notebooks

From the project root, with `.venv-quantum` active:

```powershell
jupyter notebook quantum/00_Paper_study/03_var_with_amplitude_estimation.ipynb
jupyter notebook quantum/01_math_foundations/01_gates_as_unitary_matrices.ipynb
jupyter notebook quantum/02_optics/01_polarization_as_qubit.ipynb
jupyter notebook quantum/03_quantum_mechanics/01_bell_state_entanglement.ipynb
jupyter notebook quantum/03_quantum_mechanics/02_bra_ket_operators_eigenfunctions.ipynb
jupyter notebook quantum/04_quantum_electronics/01_rabi_oscillations.ipynb
jupyter notebook quantum/04_quantum_electronics/02_semiconductor_states_and_dos.ipynb
jupyter notebook quantum/04_quantum_electronics/03_course_recap.ipynb
jupyter notebook quantum/04_quantum_electronics/04_cavity_qswitch_modelock.ipynb
jupyter notebook "quantum/05_Basics of quantum information/01_circuiti_passo_passo.ipynb"
jupyter notebook "quantum/05_Basics of quantum information/02_densita_bloch_tensori.ipynb"
jupyter notebook quantum/06_radiazione_termica_segnatura_IR/01_lezione_conduzione_diffusione.ipynb
jupyter notebook quantum/07_nonlinear_optics/01_shg_phasematch_n2.ipynb
```

Figures render inline in the notebooks. Shared helpers live in `_common/`
(still plain Python modules). Thesis paper tutorials under `tesi/papers/` remain
short `.py` scripts generated from the catalog.

> On Windows, if the Qiskit circuit drawing shows odd characters, set
> `PYTHONIOENCODING=utf-8` before running (the scripts already try to do this).

## "One commit a day" workflow

1. Pick the subject of the day.
2. Create a new numbered notebook (e.g. `02_....ipynb`) starting from the
   "Next step" suggested at the bottom of the previous notebook.
3. Run all cells and check the output.
4. Update the subject's `README.md` with a line about the work done.
5. Commit with a clear message, for example:

```bash
git add quantum/
git commit -m "optics: beam splitter as a Hadamard gate"
git push
```

## What is NOT published

The professors' material in `data/` and the RAG index in `agents/index/` are
excluded via `.gitignore` (potentially copyrighted content). Only **my code**
goes on GitHub.
