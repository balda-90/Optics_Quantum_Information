# 00 — Paper study

Sandbox / paper-study notebooks: exploratory demos tied to thesis and course
topics (Amplitude Estimation, VaR, credit risk, QML, wave packets, circuits, …).
Prefer **Jupyter notebooks** here.

## Log

| Date       | File                                         | What I did |
|------------|----------------------------------------------|------------|
| 2026-08-02 | `01_wavepackets_and_rabi.ipynb`              | Wave packet, free propagation, Rabi playground (from Matrixandode). |
| 2026-08-xx | `02_amplitude_estimation.ipynb`              | Step-by-step Amplitude Estimation (operators A and Q). |
| 2026-08-09 | `03_var_with_amplitude_estimation.ipynb`     | Value at Risk via Amplitude Estimation: portfolio P&L, CDF-as-amplitude, ideal QAE vs MC, binary-search VaR, optional Qiskit Bernoulli AE. |
| 2026-08-11 | `04_credit_at_risk.ipynb`                    | Credit VaR for correlated assets: latent factor Z, formula (11), building operator A = U + S + C, Ry encoding of default probs, MC twin of the circuit + binary-search VaR. |
| 2026-08-12 | `05_quantum_ml_advantage.ipynb`              | Classical vs hybrid vs quantum ML: scorecard, moons classification, RBF vs ZZ quantum-inspired kernel, toy VQC, scaling cartoons, barren plateaus. |
| 2026-08-13 | `06_portfolio_optimization_mc_vs_quantum.ipynb` | €50k book (RGTI, IONQ, QNTM.MI, RACE.MI, LEGN, TTWO, LGND, SMR): Monte Carlo Markowitz vs QUBO/QAOA, integer lots, honest n=8 scaling. |
| 2026-08-17 | `06_portfolio_optimization_mc_vs_quantum.ipynb` | Fair Hamming-K random-search twin vs QAOA shots; 70/30 out-of-sample frozen-ticket P&L (max DD, realized Sharpe); shot Hamming-weight diagnostic. |

## Run

```powershell
jupyter notebook quantum/00_Paper_study/02_amplitude_estimation.ipynb
jupyter notebook quantum/00_Paper_study/03_var_with_amplitude_estimation.ipynb
jupyter notebook quantum/00_Paper_study/04_credit_at_risk.ipynb
jupyter notebook quantum/00_Paper_study/05_quantum_ml_advantage.ipynb
jupyter notebook quantum/00_Paper_study/06_portfolio_optimization_mc_vs_quantum.ipynb
```
