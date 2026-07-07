"""
Black-Scholes-Merton: pricing classico vs quantistico
=====================================================

Illustra tre approcci al prezzo di un'opzione call europea:

  1. Formula analitica di Black-Scholes-Merton (soluzione chiusa)
  2. Monte Carlo classico (simulazione di traiettorie GBM)
  3. Quantum Monte Carlo semplificato (Qiskit):
       - preparazione dello stato della distribuzione log-normale
       - caricamento del payoff su qubit ancilla
       - stima dell'ampiezza attesa (proxy di Quantum Amplitude Estimation)

Dipendenze:
    pip install numpy scipy matplotlib qiskit

Esecuzione:
    python black_scholes_merton.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

from qiskit import QuantumCircuit
from qiskit.circuit.library import Initialize
from qiskit.quantum_info import Statevector


# ---------------------------------------------------------------------------
# Parametri del modello
# ---------------------------------------------------------------------------

@dataclass
class MarketParams:
    """Parametri di mercato per Black-Scholes-Merton."""
    S0: float = 100.0   # prezzo spot dell'asset
    K: float = 100.0    # strike
    r: float = 0.05     # tasso privo di rischio (annuo)
    sigma: float = 0.20 # volatilita' annua
    T: float = 1.0      # scadenza in anni


# ---------------------------------------------------------------------------
# 1. Metodo classico: formula analitica
# ---------------------------------------------------------------------------

def black_scholes_call(params: MarketParams) -> float:
    """
    Prezzo analitico di una call europea (Black-Scholes-Merton, 1973).

    C = S0 * N(d1) - K * exp(-rT) * N(d2)

    dove d1, d2 dipendono da S0, K, r, sigma, T.
    """
    S0, K, r, sigma, T = params.S0, params.K, params.r, params.sigma, params.T
    d1 = (math.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def black_scholes_put(params: MarketParams) -> float:
    """Prezzo analitico put (via parita' put-call)."""
    call = black_scholes_call(params)
    return call - params.S0 + params.K * math.exp(-params.r * params.T)


# ---------------------------------------------------------------------------
# 2. Metodo classico: Monte Carlo
# ---------------------------------------------------------------------------

def simulate_terminal_prices(params: MarketParams, n_paths: int, seed: int = 42) -> np.ndarray:
    """
    Simula prezzi terminali S_T con moto browniano geometrico (GBM):

        S_T = S0 * exp((r - 0.5*sigma^2)*T + sigma*sqrt(T)*Z),  Z ~ N(0,1)
    """
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(n_paths)
    drift = (params.r - 0.5 * params.sigma ** 2) * params.T
    diffusion = params.sigma * math.sqrt(params.T) * Z
    return params.S0 * np.exp(drift + diffusion)


def monte_carlo_call(params: MarketParams, n_paths: int = 100_000, seed: int = 42) -> Tuple[float, float]:
    """
    Stima il prezzo call via Monte Carlo:

        C ≈ exp(-rT) * E[max(S_T - K, 0)]

    Restituisce (prezzo, errore standard stimato).
    """
    S_T = simulate_terminal_prices(params, n_paths, seed)
    payoffs = np.maximum(S_T - params.K, 0.0)
    discount = math.exp(-params.r * params.T)
    mean_payoff = discount * np.mean(payoffs)
    stderr = discount * np.std(payoffs, ddof=1) / math.sqrt(n_paths)
    return mean_payoff, stderr


def monte_carlo_convergence(params: MarketParams, sample_sizes: np.ndarray, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """Errore Monte Carlo vs numero di campioni (per grafico di convergenza)."""
    analytical = black_scholes_call(params)
    errors = []
    for n in sample_sizes:
        price, _ = monte_carlo_call(params, n_paths=int(n), seed=seed)
        errors.append(abs(price - analytical))
    return sample_sizes, np.array(errors)


# ---------------------------------------------------------------------------
# 3. Metodo quantistico: Quantum Monte Carlo semplificato
# ---------------------------------------------------------------------------

def lognormal_discrete_distribution(
    params: MarketParams,
    n_qubits: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Discretizza la distribuzione log-normale di S_T su 2^n_qubits bin.

    Restituisce:
        stock_prices : prezzi S_i associati a ciascun bin
        probabilities: probabilita' p_i (normalizzate)
    """
    n_states = 2 ** n_qubits
    # Intervallo [S_min, S_max] che copre ~99.7% della massa (3 sigma log-return)
    mu_log = math.log(params.S0) + (params.r - 0.5 * params.sigma ** 2) * params.T
    sigma_log = params.sigma * math.sqrt(params.T)
    S_min = math.exp(mu_log - 3 * sigma_log)
    S_max = math.exp(mu_log + 3 * sigma_log)

    edges = np.linspace(S_min, S_max, n_states + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])

    # Probabilita' per ogni intervallo via CDF normale del log-prezzo
    log_edges = np.log(edges)
    cdf = norm.cdf(log_edges, loc=mu_log, scale=sigma_log)
    probs = np.diff(cdf)
    probs = probs / probs.sum()

    return centers, probs


def state_preparation_circuit(probabilities: np.ndarray) -> QuantumCircuit:
    """
    Circuito che prepara |psi> = sum_i sqrt(p_i) |i>.

    Usa la porta Initialize di Qiskit per codificare una distribuzione
    di probabilita' arbitraria nel registro computazionale.
    """
    n_qubits = int(math.log2(len(probabilities)))
    amplitudes = np.sqrt(probabilities)
    qc = QuantumCircuit(n_qubits, name="state_prep")
    qc.append(Initialize(amplitudes), list(range(n_qubits)))
    return qc


def payoff_loading_circuit(
    stock_prices: np.ndarray,
    probabilities: np.ndarray,
    strike: float,
    n_qubits: int,
) -> QuantumCircuit:
    """
    Circuito completo per QMC semplificato:

        |0...0>  --[state prep]-->  sum sqrt(p_i)|i>
        |0> ancilla --[payoff]-->   rotazione Ry(2*arcsin(sqrt(f_i))) controllata

    dove f_i = payoff_i / max_payoff, payoff_i = max(S_i - K, 0).
    """
    payoffs = np.maximum(stock_prices - strike, 0.0)
    max_payoff = payoffs.max()
    if max_payoff <= 0:
        f = np.zeros_like(payoffs)
    else:
        f = payoffs / max_payoff

    qc = QuantumCircuit(n_qubits + 1, name="qmc_circuit")
    ancilla = n_qubits

    # State preparation sul registro principale
    prep = state_preparation_circuit(probabilities)
    qc.compose(prep, qubits=range(n_qubits), inplace=True)

    # Caricamento payoff: per ogni stato |i>, ruota l'ancilla di theta_i = 2*arcsin(sqrt(f_i))
    for i, fi in enumerate(f):
        if fi <= 1e-12:
            continue
        theta = 2 * math.asin(math.sqrt(fi))
        # Decomposizione multi-controllata: Ry(theta) su ancilla controllata da |i>
        _apply_multicontrolled_ry(qc, theta, control_state=i, n_controls=n_qubits, target=ancilla)

    return qc


def _apply_multicontrolled_ry(
    qc: QuantumCircuit,
    theta: float,
    control_state: int,
    n_controls: int,
    target: int,
) -> None:
    """Applica Ry(theta) controllato dallo stato binario |control_state>."""
    flipped = []
    for bit in range(n_controls):
        if not (control_state >> bit) & 1:
            qc.x(bit)
            flipped.append(bit)

    controls = list(range(n_controls))
    qc.mcry(theta, controls, target, None)

    for bit in flipped:
        qc.x(bit)


def quantum_monte_carlo_call(
    params: MarketParams,
    n_qubits: int = 3,
) -> Tuple[float, float, QuantumCircuit]:
    """
    Stima il prezzo call via Quantum Monte Carlo semplificato.

    Procedura:
      1. Discretizza S_T su 2^n_qubits stati
      2. Prepara |psi> = sum sqrt(p_i)|i>
      3. Carica payoff sull'ancilla (ampiezza P(ancilla=1) proporzionale al payoff medio)
      4. Misura P(ancilla=1) con StatevectorSampler -> stima E[payoff/max]

    Il prezzo finale: C ≈ exp(-rT) * max_payoff * P(ancilla=1)

    Nota teorica: con Quantum Amplitude Estimation (QAE) completo,
    la precisione epsilon si ottiene con O(1/epsilon) query invece di O(1/epsilon^2).
    """
    stock_prices, probs = lognormal_discrete_distribution(params, n_qubits)
    payoffs = np.maximum(stock_prices - params.K, 0.0)
    max_payoff = payoffs.max()

    circuit = payoff_loading_circuit(stock_prices, probs, params.K, n_qubits)

    # Simulazione esatta via statevector: P(ancilla=1) = sum_i p_i * f_i
    statevector = Statevector.from_instruction(circuit)
    ancilla_index = n_qubits  # ultimo qubit e' l'ancilla
    p_ancilla_1 = sum(
        abs(amp) ** 2
        for i, amp in enumerate(statevector)
        if ((i >> ancilla_index) & 1) == 1
    )

    discount = math.exp(-params.r * params.T)
    quantum_price = discount * max_payoff * p_ancilla_1

    # Prezzo classico sulla stessa griglia discretizzata (riferimento)
    discrete_price = discount * np.sum(probs * payoffs)

    return quantum_price, discrete_price, circuit


def theoretical_qae_advantage(epsilon: float) -> Tuple[int, int]:
    """
    Confronto query necessarie per precisione epsilon:

        Monte Carlo classico:  O(1/epsilon^2)
        Quantum Amplitude Est.: O(1/epsilon)

    Restituisce (n_classical, n_quantum) per il confronto didattico.
    """
    n_classical = math.ceil(1 / epsilon ** 2)
    n_quantum = math.ceil(1 / epsilon)
    return n_classical, n_quantum


# ---------------------------------------------------------------------------
# Visualizzazione
# ---------------------------------------------------------------------------

def plot_results(
    params: MarketParams,
    mc_sizes: np.ndarray,
    mc_errors: np.ndarray,
    prices: dict,
) -> None:
    """Genera grafici comparativi e li salva su file."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Convergenza Monte Carlo
    ax = axes[0]
    ax.loglog(mc_sizes, mc_errors, "o-", color="steelblue", label="Errore |MC - analitico|")
    ax.axhline(y=0.01, color="gray", linestyle="--", alpha=0.7, label="epsilon = 0.01")
    ax.set_xlabel("Numero campioni Monte Carlo")
    ax.set_ylabel("Errore assoluto")
    ax.set_title("Convergenza Monte Carlo classico\n(errori ~ 1/sqrt(N))")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Confronto prezzi
    ax = axes[1]
    labels = list(prices.keys())
    values = list(prices.values())
    colors = ["#2ecc71", "#3498db", "#9b59b6", "#e74c3c"]
    bars = ax.bar(labels, values, color=colors[: len(labels)])
    ax.axhline(y=prices["Analitico (BSM)"], color="black", linestyle="--", linewidth=1.5, label="Riferimento BSM")
    ax.set_ylabel("Prezzo call")
    ax.set_title("Confronto metodi di pricing")
    ax.legend()
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{val:.3f}", ha="center", fontsize=9)

    plt.suptitle(
        f"Black-Scholes-Merton  |  S0={params.S0}, K={params.K}, "
        f"r={params.r}, sigma={params.sigma}, T={params.T}",
        fontsize=11,
    )
    plt.tight_layout()
    out_path = "black_scholes_comparison.png"
    plt.savefig(out_path, dpi=150)
    print(f"\nGrafico salvato in: {out_path}")
    if plt.get_backend().lower() != "agg":
        plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    params = MarketParams()

    print("=" * 60)
    print("BLACK-SCHOLES-MERTON: Classico vs Quantum Computing")
    print("=" * 60)
    print(f"\nParametri: S0={params.S0}, K={params.K}, r={params.r}, "
          f"sigma={params.sigma}, T={params.T} anni\n")

    # --- 1. Analitico ---
    price_analytical = black_scholes_call(params)
    print(f"[1] Formula analitica BSM:     {price_analytical:.4f}")

    # --- 2. Monte Carlo classico ---
    mc_price, mc_stderr = monte_carlo_call(params, n_paths=200_000)
    print(f"[2] Monte Carlo classico:      {mc_price:.4f}  (+/- {mc_stderr:.4f})")

    # --- 3. Quantum Monte Carlo ---
    print("\n[3] Quantum Monte Carlo (Qiskit, 2^3 = 8 stati discretizzati)...")
    q_price, discrete_ref, circuit = quantum_monte_carlo_call(params, n_qubits=3)
    print(f"    Prezzo quantistico (stima):  {q_price:.4f}")
    print(f"    Riferimento griglia discr.:  {discrete_ref:.4f}")
    print(f"    Circuito: {circuit.num_qubits} qubit, depth={circuit.depth()}")

    # --- Vantaggio teorico QAE ---
    eps = 0.01
    n_class, n_quant = theoretical_qae_advantage(eps)
    print(f"\n[4] Vantaggio teorico QAE (epsilon={eps}):")
    print(f"    Campioni MC classico:  ~{n_class:,}  (O(1/eps^2))")
    print(f"    Query QAE quantistico: ~{n_quant:,}  (O(1/eps))")
    print(f"    Speedup teorico:       ~{n_class // n_quant}x")

    # --- Convergenza MC ---
    mc_sizes = np.array([100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000])
    _, mc_errors = monte_carlo_convergence(params, mc_sizes)

    prices = {
        "Analitico (BSM)": price_analytical,
        "Monte Carlo": mc_price,
        "QMC (quantum)": q_price,
        "Griglia discr.": discrete_ref,
    }
    plot_results(params, mc_sizes, mc_errors, prices)

    print("\n" + "=" * 60)
    print("NOTE DIDATTICHE")
    print("=" * 60)
    print("""
Il modello Black-Scholes-Merton assume:
  - mercato efficiente, nessun costo di transazione
  - tasso privo di rischio r costante
  - volatilita' sigma costante
  - moto browniano geometrico del prezzo

Metodi classici:
  - Formula chiusa: esatta, istantanea (solo opzioni europee semplici)
  - Monte Carlo: flessibile (path-dependent, american options), errore O(1/sqrt(N))

Metodo quantistico (Quantum Monte Carlo + QAE):
  1. Codifica la distribuzione del payoff in uno stato quantistico
  2. Oracle di payoff + Quantum Amplitude Estimation
  3. Convergenza O(1/epsilon) vs O(1/epsilon^2) classico

Limiti attuali: servono hardware fault-tolerant e molti qubit per
vantaggi reali su problemi finanziari industriali; oggi e' mainly NISQ research.
""")


if __name__ == "__main__":
    main()
