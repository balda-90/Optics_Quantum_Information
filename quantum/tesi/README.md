# Thesis — Quantum Computing in Finance

Exploration of the bibliography stored locally under `data/100_TESI/` (not
published on GitHub). This folder contains **reproducible scripts** and a
**notebook** that map paper objectives to code.

## Literature levels

| Level | Folder | Focus |
|-------|--------|-------|
| L0 | `Livello_0_Fondamenta` | QAE, QML, Monte Carlo foundations |
| L1 | `Livello_1_Survey_Industry` | Industry readiness & surveys |
| L2A | `Livello_2A_Portfolio_Optimization` | QUBO, VQE, annealing |
| L2B | `Livello_2B_Risk_MonteCarlo_Derivatives` | Option pricing, risk |
| L2C | `Livello_2C_Quantum_Machine_Learning` | QGNN, fraud |
| L2D | `Livello_2D_Post_Quantum_Cryptography` | PQC migration |
| L3 | `Livello_3_Tesi_Riferimento` | Reference theses |

See `papers_catalog.yaml` for titles, arXiv IDs and objectives.

## Files

| File | Maps to |
|------|---------|
| `00_thesis_literature_map.ipynb` | Interactive overview of catalog + BoF survey |
| `01_quantum_amplitude_estimation.py` | Brassard QAE; Rebentrost MC speedup |
| `02_european_option_monte_carlo.py` | Stamatopoulos classical MC baseline |
| `03_portfolio_optimization_qubo.py` | Level 2A portfolio / QUBO |
| `04_industry_survey_themes.py` | Bank of Finland 2025 themes |

## Run

```powershell
.\.venv-quantum\Scripts\Activate.ps1
jupyter notebook quantum/tesi/00_thesis_literature_map.ipynb
python quantum/tesi/01_quantum_amplitude_estimation.py
```

Plots are saved under each script's `output/` folder.

## Download papers locally

From the repo root (papers stay in `data/`, gitignored):

```powershell
powershell -ExecutionPolicy Bypass -File data/100_TESI/download_papers.ps1
```
