"""
Generate beginner-friendly paper tutorials under quantum/tesi/papers/.

Run from repo root:
    python quantum/tesi/materialize_paper_tutorials.py
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
PAPERS_DIR = ROOT / "papers"
CATALOG_PATH = ROOT / "papers_catalog.yaml"

FOLDER_MAP = {
    "L0": "L0_fondamenta",
    "L1": "L1_survey",
    "L2A": "L2A_portfolio",
    "L2B": "L2B_risk",
    "L2C": "L2C_qml",
    "L2D": "L2D_pqc",
    "L3": "L3_thesis_ref",
}

SLUG_ORDER: list[tuple[str, str]] = [
    ("L0", "L0_01_orus_2019"),
    ("L0", "L0_02_egger_2020"),
    ("L0", "L0_03_rebentrost_mc_2018"),
    ("L0", "L0_04_brassard_qae_2002"),
    ("L0", "L0_05_rebentrost_qml_2014"),
    ("L1", "L1_01_qml_quant_finance_2024"),
    ("L1", "L1_02_fca_regulatory_2024"),
    ("L1", "L1_03_mdpi_practical_2025"),
    ("L1", "L1_04_portfolio_blockchain_2025"),
    ("L1", "L1_05_doosti_qml_review_2024"),
    ("L1", "L1_06_bof_finland_2025"),
    ("L2A", "L2A_01_jpmorgan_decomposition_2025"),
    ("L2A", "L2A_02_bbva_vqe_2025"),
    ("L2A", "L2A_03_hybrid_discretization_2025"),
    ("L2A", "L2A_04_poqa_framework_2024"),
    ("L2A", "L2A_05_annealing_e2e_2025"),
    ("L2A", "L2A_06_ionq_large_scale_2026"),
    ("L2B", "L2B_01_stamatopoulos_options_2020"),
    ("L2B", "L2B_02_goldman_market_risk_2022"),
    ("L2B", "L2B_03_qmc_risk_2024"),
    ("L2B", "L2B_04_counterparty_credit_2025"),
    ("L2C", "L2C_01_fraud_qgnn_2024"),
    ("L2D", "L2D_01_pqc_roadmap_2025"),
    ("L3", "L3_01_jauron_thesis_2022"),
    ("L3", "L3_02_berube_thesis_2024"),
]

# Rich per-paper educational content + demo code (keyed by slug).
PAPERS: dict[str, dict[str, Any]] = {
    "L0_01_orus_2019": {
        "subtitle": "Mapping finance problems to quantum algorithms",
        "finance_problem": [
            "Banks face many computationally heavy tasks: pricing exotic derivatives, "
            "optimizing large portfolios, simulating credit risk, and running "
            "anti-fraud models. Classical methods often scale poorly when accuracy "
            "requirements grow.",
            "Orus et al. (2019) ask a practical question: which finance problems "
            "are natural fits for quantum algorithms, and which are still far away?",
        ],
        "paper_idea": [
            "The paper is a structured survey. It groups finance use cases "
            "(optimization, simulation, machine learning) and links each to "
            "quantum building blocks such as QAOA, VQE, amplitude estimation, "
            "and quantum annealing.",
            "Think of it as a roadmap index: not one algorithm, but a map from "
            "business pain points to quantum toolkits.",
        ],
        "concepts": [
            ("Combinatorial optimization", "Choosing the best option among exponentially many discrete choices, like selecting assets in a portfolio."),
            ("Quantum simulation", "Using a controllable quantum system to mimic another hard-to-simulate system, such as stochastic market dynamics."),
            ("Near-term vs fault-tolerant", "Today's noisy devices can run shallow circuits; fault-tolerant machines promise much larger algorithms later."),
        ],
        "analogy": "Orus et al. is like a city transit map for quantum finance: it does not drive the train, but shows which line (algorithm family) reaches which destination (finance task).",
        "limitations": [
            "Survey papers summarize possibilities; they do not guarantee quantum advantage on real bank data today.",
            "Hardware noise and data encoding costs are often under-estimated in early roadmaps.",
            "Many cited speedups assume ideal oracles and fault-tolerant resources.",
        ],
        "recap": [
            "Finance problems cluster into optimization, simulation, and learning.",
            "Quantum algorithms are matched by problem structure, not by hype.",
            "Orus 2019 is a foundational map for later applied papers.",
        ],
        "next_steps": [
            "Read Egger et al. 2020 for IBM's updated finance roadmap.",
            "Run script 01 in quantum/tesi/ for QAE error scaling intuition.",
            "Skim your portfolio optimization QUBO demo in quantum/tesi/03_portfolio_optimization_qubo.py.",
        ],
        "imports_extra": """import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _common import savefig""",
        "demo_fn": '''def run_demo() -> None:
    """Count finance tasks by suggested quantum approach (toy taxonomy)."""
    categories = {
        "Portfolio / QUBO": 4,
        "Derivatives / QAE": 3,
        "Risk / QMC": 3,
        "ML / QML": 2,
    }
    labels = list(categories.keys())
    counts = np.array(list(categories.values()), dtype=float)
    explain(
        "Below we simulate how a survey might tag finance tasks by algorithm family.",
        f"Total mapped tasks in this toy index: {int(counts.sum())}",
    )
    for label, c in zip(labels, counts):
        print(f"  {label:22s} -> {int(c)} papers/use-cases")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(labels, counts, color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"])
    ax.set_xlabel("Number of mapped use cases (illustrative)")
    ax.set_title("Orus-style mapping: finance task -> quantum family")
    ax.grid(axis="x", alpha=0.3)
    path = savefig(fig, __file__, "orus_finance_map.png")
    plt.close(fig)
    print(f"\\n  Plot saved to: {path}")''',
    },
    "L0_02_egger_2020": {
        "subtitle": "IBM state-of-the-art and near-term finance roadmap",
        "finance_problem": [
            "Financial institutions need a realistic timeline: when can quantum "
            "computing help with production workloads, not just toy models?",
            "Egger et al. (2020) evaluate algorithms against near-term hardware "
            "constraints and classical baselines.",
        ],
        "paper_idea": [
            "The authors update the finance quantum landscape with emphasis on "
            "variational algorithms, annealing, and amplitude estimation pipelines.",
            "They discuss what is feasible on NISQ devices versus what needs "
            "error-corrected machines.",
        ],
        "concepts": [
            ("NISQ", "Noisy Intermediate-Scale Quantum: devices with tens–hundreds of qubits and imperfect gates."),
            ("Variational quantum algorithm", "A hybrid loop where a classical optimizer tunes quantum circuit parameters."),
            ("Resource estimation", "Counting qubits, circuit depth, and shots needed to beat a classical method."),
        ],
        "analogy": "Egger's roadmap is like a product release plan: some features ship in beta (NISQ pilots), others need the next major platform (fault tolerance).",
        "limitations": [
            "Roadmaps age quickly as hardware and classical algorithms improve.",
            "Pilot success on synthetic data may not transfer to messy production datasets.",
            "Integration with existing risk systems is non-trivial.",
        ],
        "recap": [
            "Egger 2020 bridges theory and near-term engineering reality.",
            "Finance use cases must be judged with resource budgets.",
            "Hybrid classical-quantum workflows are the practical default.",
        ],
        "next_steps": [
            "Compare with Orus 2019 to see how priorities shifted.",
            "Explore VQE portfolio demo in L2A_02_bbva_vqe_2025 tutorial.",
            "Read Goldman 2022 for risk-specific resource estimates.",
        ],
        "imports_extra": "from scipy.stats import norm",
        "demo_fn": '''def run_demo() -> None:
    """Maturity score vs required qubits for three finance workloads."""
    workloads = ["Portfolio VQE", "Option QAE", "Fraud QML"]
    maturity = np.array([0.55, 0.40, 0.30])
    qubits_needed = np.array([80, 200, 120])
    explain(
        "We plot illustrative maturity (0–1) against estimated qubit needs.",
        "Higher maturity means closer to industry pilot; qubits are rough order-of-magnitude.",
    )
    for w, m, q in zip(workloads, maturity, qubits_needed):
        print(f"  {w:16s} | maturity={m:.2f} | est. qubits={q}")
    # Sigmoid readiness curve vs year
    years = np.linspace(2020, 2030, 50)
    readiness = 1 / (1 + np.exp(-(years - 2027) / 1.2))
    print(f"\\n  Projected industry readiness in 2026: {readiness[years >= 2026][0]:.2f}")''',
    },
    "L0_03_rebentrost_mc_2018": {
        "subtitle": "Quantum Monte Carlo pricing with amplitude estimation",
        "finance_problem": [
            "Derivative pricing often relies on Monte Carlo simulation. To reduce "
            "pricing error by a factor of 10, classical MC typically needs 100× "
            "more samples because error scales like 1/√N.",
            "For exotics and multi-asset products, this becomes expensive in "
            "production risk engines.",
        ],
        "paper_idea": [
            "Rebentrost et al. (2018) combine quantum state preparation with "
            "Quantum Amplitude Estimation (QAE) to estimate expected payoffs.",
            "The promise is a query complexity scaling closer to 1/N instead of 1/√N, "
            "which is highly attractive for risk-sensitive pricing.",
        ],
        "concepts": [
            ("Quantum Monte Carlo", "Encode random scenarios in superposition and estimate payoff amplitudes."),
            ("Oracle", "A quantum subroutine that marks states where a condition (e.g. positive payoff) holds."),
            ("Quadratic speedup", "QAE can reduce sample/oracle queries quadratically vs classical MC in ideal settings."),
        ],
        "analogy": "Classical MC is like polling random voters one-by-one; QAE is like a clever counting algorithm that extracts the election result with fewer questions—if the polling machine is perfect.",
        "limitations": [
            "Loading financial distributions into quantum states is costly.",
            "Current hardware cannot run full fault-tolerant QAE at scale.",
            "Constant factors and error correction overhead may erode speedups.",
        ],
        "recap": [
            "Rebentrost 2018 connects derivative pricing to QAE.",
            "The headline is better scaling in oracle queries.",
            "State preparation is often the hidden bottleneck.",
        ],
        "next_steps": [
            "Run L0_04_brassard_qae_2002 for the original QAE theory.",
            "Run quantum/tesi/02_european_option_monte_carlo.py for classical baseline.",
            "Open L2B_01_stamatopoulos_options_2020 for JPMorgan implementation view.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Compare classical MC error scaling vs ideal QAE bound."""
    p_true = 0.42
    shots = np.array([20, 50, 100, 200, 500, 1000, 2000])
    rng = np.random.default_rng(7)
    mc_errors = []
    for s in shots:
        trials = [abs((rng.random(s) < p_true).mean() - p_true) for _ in range(300)]
        mc_errors.append(float(np.mean(trials)))
    qae_bound = np.pi / (2 * shots)
    explain(f"Estimating probability p={p_true} (e.g. ITM indicator).")
    print("\\n  shots | MC error | QAE bound")
    for s, mc, qae in zip(shots[::2], mc_errors[::2], qae_bound[::2]):
        print(f"  {s:5d} | {mc:.4f}   | {qae:.4f}")
    ratio = mc_errors[-1] / qae_bound[-1]
    print(f"\\n  At {shots[-1]} shots, MC error is ~{ratio:.1f}x the ideal QAE bound.")''',
    },
    "L0_04_brassard_qae_2002": {
        "subtitle": "Original Quantum Amplitude Estimation paper",
        "finance_problem": [
            "Many finance metrics are probabilities or expectations: default events, "
            "positive payoff indicators, breach of VaR thresholds.",
            "Classical sampling needs many trials for high precision.",
        ],
        "paper_idea": [
            "Brassard et al. (2002) introduce Quantum Amplitude Estimation and "
            "Quantum Amplitude Amplification (generalizing Grover search).",
            "Given a quantum state with amplitude a, QAE estimates a using O(1/ε) "
            "queries instead of O(1/ε²) classical samples.",
        ],
        "concepts": [
            ("Amplitude", "The √probability component of a quantum state coefficient."),
            ("Grover iterator", "Repeated reflection operations that amplify target amplitudes."),
            ("Phase estimation", "Extracts eigenphases of unitary operators to read amplitudes."),
        ],
        "analogy": "Amplitude amplification is like turning up the volume on one instrument in an orchestra without replaying the whole concert many times.",
        "limitations": [
            "Requires coherent quantum oracles and long circuits for high precision.",
            "Financial payoff oracles must be reversible and implementable.",
            "Error rates compound with depth on real devices.",
        ],
        "recap": [
            "QAE is the theoretical engine behind many finance speedup claims.",
            "Amplification + phase estimation achieves 1/N-type scaling.",
            "Finance papers cite Brassard as the core reference.",
        ],
        "next_steps": [
            "Study Grover iterations in the demo below.",
            "Read Rebentrost MC 2018 for finance application.",
            "Try quantum/tesi/01_quantum_amplitude_estimation.py.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Simulate Grover-like amplitude amplification on a 1-qubit toy model."""
    theta = np.pi / 5  # initial amplitude a = sin(theta)
    a = np.sin(theta) ** 2
    explain(f"Target amplitude a = sin²(theta) = {a:.4f}")
    state = np.array([np.cos(theta), np.sin(theta)], dtype=complex)
    # Grover reflection about |0> and about psi
    def reflect_about_zero(psi):
        return np.array([psi[0], -psi[1]])
    def reflect_about_psi(psi, ref):
        proj = np.vdot(ref, psi) * ref
        return 2 * proj - psi
    amps = [a]
    psi = state.copy()
    for k in range(1, 6):
        psi = reflect_about_psi(reflect_about_zero(psi), state)
        psi = psi / np.linalg.norm(psi)
        amps.append(float(np.abs(psi[1]) ** 2))
    print("\\n  Grover iterations -> amplified probability:")
    for k, p in enumerate(amps):
        print(f"    k={k}: P(target)={p:.4f}")''',
    },
    "L0_05_rebentrost_qml_2014": {
        "subtitle": "Quantum algorithms for machine learning foundations",
        "finance_problem": [
            "Finance ML tasks include credit scoring, fraud detection, and "
            "customer segmentation. Kernel methods and distance metrics are central.",
            "Classical ML on high-dimensional features can be slow at scale.",
        ],
        "paper_idea": [
            "Rebentrost et al. (2014) present quantum linear algebra tools and "
            "distance-based classification ideas (e.g. HHL-related techniques).",
            "They lay groundwork for QML pipelines that finance papers reuse later.",
        ],
        "concepts": [
            ("Quantum feature map", "Encodes classical vectors into quantum states."),
            ("Kernel", "A similarity function between data points; quantum circuits can induce kernels."),
            ("HHL", "Harrow-Hassidim-Lloyd algorithm for linear systems—promising but resource-heavy."),
        ],
        "analogy": "QML feature maps are like translating spreadsheets into a musical score the quantum computer can play—similar data, very different representation.",
        "limitations": [
            "HHL needs fault-tolerant resources for practical finance datasets.",
            "Data loading remains O(n) unless structures are exploited.",
            "Many QML demos use tiny synthetic sets only.",
        ],
        "recap": [
            "Rebentrost 2014 connects linear algebra and learning on quantum hardware.",
            "Distance/kernel viewpoint links to later fraud and QML surveys.",
            "Not finance-specific, but foundational for L1/L2C papers.",
        ],
        "next_steps": [
            "Open L1_01_qml_quant_finance_2024 survey tutorial.",
            "Try L2C_01_fraud_qgnn_2024 for graph-based fraud detection.",
            "Review Doosti 2024 compact QML taxonomy.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Quantum-inspired distance kernel between two 2D finance feature vectors."""
    x = np.array([1.0, 0.2])
    y = np.array([0.7, 0.9])
    phi = lambda v: np.array([v[0], v[1], v[0] * v[1]])  # simple feature map
    fx, fy = phi(x), phi(y)
    k_xy = float(np.dot(fx, fy))
    d_xy = float(np.linalg.norm(fx - fy))
    explain("Two customer feature vectors x and y (normalized toy features).")
    print(f"  x = {x}, y = {y}")
    print(f"  kernel k(x,y) = {k_xy:.4f}")
    print(f"  embedded distance ||phi(x)-phi(y)|| = {d_xy:.4f}")
    angle = np.arccos(k_xy / (np.linalg.norm(fx) * np.linalg.norm(fy)))
    print(f"  angle in feature space = {np.degrees(angle):.2f} degrees")''',
    },
    "L1_01_qml_quant_finance_2024": {
        "subtitle": "Survey of QML techniques applied to quantitative finance",
        "finance_problem": [
            "Quant teams want to know which QML methods are credible for time-series "
            "forecasting, classification, and anomaly detection.",
            "The 2024 survey maps techniques to datasets and evaluation metrics.",
        ],
        "paper_idea": [
            "Authors categorize QML models (variational classifiers, quantum kernels, "
            "QNNs) and align them with finance tasks like volatility forecasting "
            "and credit scoring.",
        ],
        "concepts": [
            ("Variational classifier", "Parameterized quantum circuit trained with classical optimizers."),
            ("Barren plateaus", "Flat loss landscapes that make training hard at scale."),
            ("NISQ-friendly QML", "Shallow circuits designed for today's hardware limits."),
        ],
        "analogy": "This survey is a menu of QML dishes with finance pairing suggestions—not every dish is ready to serve in production.",
        "limitations": [
            "Benchmarks vary widely; fair comparison to classical ML is hard.",
            "Many studies use pre-quantum-era datasets without market regime shifts.",
            "Regulatory explainability requirements are not always addressed.",
        ],
        "recap": [
            "QML in finance spans forecasting, classification, and clustering.",
            "Hardware depth and data encoding dictate feasibility.",
            "Use surveys to shortlist algorithms before deep implementation.",
        ],
        "next_steps": [
            "Read Doosti 2024 for a shorter taxonomy.",
            "Run L2C_01_fraud_qgnn_2024 hands-on graph demo.",
            "Check FCA 2024 regulatory perspective.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Score QML techniques for three finance tasks (toy rubric)."""
    techniques = ["Quantum kernel SVM", "VQC classifier", "QGAN synthetic data"]
    tasks = ["Credit scoring", "Vol forecasting", "Fraud graphs"]
    scores = np.array([[0.7, 0.5, 0.4], [0.6, 0.6, 0.5], [0.3, 0.4, 0.6]])
    explain("Rubric scores (0–1) for technique-task fit (illustrative).")
    for i, tech in enumerate(techniques):
        best_j = int(np.argmax(scores[i]))
        print(f"  {tech:22s} -> best fit: {tasks[best_j]} ({scores[i, best_j]:.2f})")
    print(f"\\n  Mean score per technique: {scores.mean(axis=1)}")''',
    },
    "L1_02_fca_regulatory_2024": {
        "subtitle": "UK FCA view on quantum in financial services",
        "finance_problem": [
            "Regulators must balance innovation with market stability, consumer "
            "protection, and operational resilience.",
            "Quantum computing brings both opportunity (better models) and threat "
            "(breaking classical cryptography).",
        ],
        "paper_idea": [
            "The FCA discussion paper frames how firms should assess quantum readiness, "
            "third-party risk, and governance for pilot projects.",
            "It highlights post-quantum cryptography migration as a near-term priority.",
        ],
        "concepts": [
            ("Operational resilience", "Ability to continue critical services through technology disruptions."),
            ("Model risk management", "Validating that new models (including quantum) are fit for purpose."),
            ("PQC migration", "Upgrading crypto systems before large-scale quantum attacks become realistic."),
        ],
        "analogy": "The FCA paper is the building inspector's checklist before you install a new power system in a skyscraper bank.",
        "limitations": [
            "Regulatory guidance evolves; local rules differ by jurisdiction.",
            "Firms may treat quantum as R&D without operational integration plans.",
            "PQC timelines are uncertain but migration is lengthy.",
        ],
        "recap": [
            "Regulators see quantum as strategic, not just academic.",
            "Risk management and crypto migration are top themes.",
            "Governance must precede flashy pilots.",
        ],
        "next_steps": [
            "Read L2D_01_pqc_roadmap_2025 for migration timelines.",
            "Review Bank of Finland 2025 readiness survey.",
            "Map internal crypto inventory before quantum pilots.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Weighted risk-opportunity index for quantum adoption areas."""
    areas = ["Derivatives pricing", "Portfolio opt", "Fraud ML", "Core banking crypto"]
    opportunity = np.array([0.7, 0.6, 0.5, 0.2])
    risk = np.array([0.4, 0.5, 0.4, 0.9])
    net = opportunity - risk
    explain("Net score = opportunity - risk (toy regulatory lens).")
    for a, o, r, n in zip(areas, opportunity, risk, net):
        print(f"  {a:22s} | opp={o:.1f} risk={r:.1f} | net={n:+.1f}")
    print(f"\\n  Highest priority concern: {areas[int(np.argmax(risk))]}")''',
    },
    "L1_03_mdpi_practical_2025": {
        "subtitle": "Practitioner-oriented review of QC finance applications",
        "finance_problem": [
            "Practitioners need concrete workflows: data prep, algorithm choice, "
            "hardware access, and success metrics—not just asymptotic speedups.",
        ],
        "paper_idea": [
            "MDPI 2025 emphasizes practical pipelines for optimization and simulation, "
            "including hybrid orchestration and benchmarking against classical stacks.",
        ],
        "concepts": [
            ("Hybrid workflow", "Classical pre/post-processing wrapped around quantum kernels."),
            ("Benchmarking", "Measuring wall-clock time, cost, and accuracy—not qubits alone."),
            ("Vendor stack", "Cloud quantum access via IBM, IonQ, D-Wave, etc."),
        ],
        "analogy": "A practitioner review is the workshop manual; foundational papers are the physics textbook.",
        "limitations": [
            "Cloud queue times can erase theoretical speedups.",
            "Reproducibility across hardware generations is weak.",
            "Skills gap: few teams know finance and quantum equally well.",
        ],
        "recap": [
            "Practical papers focus on end-to-end integration.",
            "Benchmark honestly against your classical production baseline.",
            "Hybrid designs are the default near-term pattern.",
        ],
        "next_steps": [
            "Run L2A_05_annealing_e2e_2025 for a full optimization pipeline.",
            "Compare JPMorgan decomposition tutorial.",
            "Document classical baseline before any quantum pilot.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """End-to-end latency budget for a hybrid portfolio pilot (toy ms)."""
    stages = ["Data ETL", "QUBO build", "Quantum job", "Decode + validate"]
    classical_ms = np.array([120, 40, 0, 30])
    hybrid_ms = np.array([120, 55, 800, 45])
    explain("Wall-clock breakdown: classical-only vs hybrid cloud job.")
    for s, c, h in zip(stages, classical_ms, hybrid_ms):
        print(f"  {s:16s} | classical {c:4.0f} ms | hybrid {h:4.0f} ms")
    print(f"\\n  Total classical: {classical_ms.sum():.0f} ms | hybrid: {hybrid_ms.sum():.0f} ms")''',
    },
    "L1_04_portfolio_blockchain_2025": {
        "subtitle": "Survey linking portfolio optimization and quantum blockchain",
        "finance_problem": [
            "Portfolio decisions increasingly interact with tokenized assets and "
            "distributed ledgers. Optimization must respect settlement and custody constraints.",
        ],
        "paper_idea": [
            "The survey connects quantum optimization methods with blockchain-inspired "
            "distributed portfolio governance and smart-contract execution.",
        ],
        "concepts": [
            ("Tokenized assets", "On-chain representations of traditional securities."),
            ("Smart contract", "Automated rules for rebalancing or collateral management."),
            ("QUBO on chain", "Optimization results committed as verifiable on-chain proposals."),
        ],
        "analogy": "Quantum optimization proposes the portfolio; blockchain is the notary and automated clerk that records and executes it.",
        "limitations": [
            "On-chain quantum solvers are not realistic; oracles bridge off-chain compute.",
            "Latency and privacy conflict with transparent ledgers.",
            "Regulatory treatment of tokenized funds varies.",
        ],
        "recap": [
            "Optimization and settlement layers should be designed together.",
            "Quantum solvers likely stay off-chain in near term.",
            "Survey papers help spot cross-domain integration risks.",
        ],
        "next_steps": [
            "Study PO-QA framework tutorial L2A_04_poqa_framework_2024.",
            "Review BBVA VQE dynamic portfolio paper.",
            "List custody constraints before encoding QUBOs.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Simulate on-chain commit of optimal weights hash vs classical rebalance."""
    n_assets = 4
    weights = np.array([0.35, 0.25, 0.20, 0.20])
    prices = np.array([100, 50, 80, 120], dtype=float)
    nav = 1_000_000
    holdings = np.round(weights * nav / prices).astype(int)
    checksum = int(np.sum(holdings * prices) % 9973)
    explain("Toy portfolio: weights -> integer holdings -> simple checksum 'on-chain'.")
    print(f"  weights = {weights}")
    print(f"  holdings (shares) = {holdings}")
    print(f"  checksum tag for ledger = {checksum}")''',
    },
    "L1_05_doosti_qml_review_2024": {
        "subtitle": "Compact QML taxonomy for financial services",
        "finance_problem": [
            "Financial services teams need a short map of QML algorithms without "
            "reading dozens of physics papers.",
        ],
        "paper_idea": [
            "Doosti 2024 provides a brief taxonomy: supervised/unsupervised QML, "
            "kernels, generative models, and finance use-case examples.",
        ],
        "concepts": [
            ("QNN", "Quantum neural network: layered parameterized circuits."),
            ("QSVM", "Quantum support vector machine using quantum feature maps."),
            ("QPCA", "Quantum principal component analysis for dimensionality reduction."),
        ],
        "analogy": "Doosti is the pocket glossary; the 2024 full QML finance survey is the encyclopedia.",
        "limitations": [
            "Brief reviews omit implementation detail.",
            "Rapid field growth makes taxonomies incomplete quickly.",
            "Empirical evidence in finance remains limited.",
        ],
        "recap": [
            "Taxonomy helps you name and classify QML approaches.",
            "Match algorithm family to data type (tabular, graph, series).",
            "Use as a study guide before thesis-level implementations.",
        ],
        "next_steps": [
            "Compare with L1_01_qml_quant_finance_2024.",
            "Run fraud QGNN demo for graph use case.",
            "Pick one algorithm family for a course mini-project.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Classify finance datasets by suggested QML family."""
    datasets = [
        ("Wire transfer logs", "QSVM / VQC"),
        ("Trader graph", "QGNN"),
        ("Yield curves", "QPCA + regressor"),
    ]
    explain("Toy mapping from data modality to QML family (Doosti-style).")
    for name, fam in datasets:
        print(f"  {name:20s} -> {fam}")''',
    },
    "L1_06_bof_finland_2025": {
        "subtitle": "Is the financial sector ready for quantum computing?",
        "finance_problem": [
            "Central banks and supervisors worry about systemic readiness: skills, "
            "vendor dependence, crypto risk, and competitive asymmetry.",
        ],
        "paper_idea": [
            "Bank of Finland survey synthesizes industry interviews and literature on "
            "readiness, opportunities, and threat scenarios including quantum attacks on banking infra.",
        ],
        "concepts": [
            ("Readiness index", "Composite score across talent, strategy, infrastructure, and governance."),
            ("Quantum threat horizon", "Estimated years until cryptographically relevant quantum computers."),
            ("Strategic optionality", "Investing in pilots to avoid being locked out later."),
        ],
        "analogy": "The BoF report is a weather forecast for a storm that may arrive in 5–15 years—you still fix the roof now.",
        "limitations": [
            "Survey samples may skew toward advanced institutions.",
            "Readiness scores are subjective.",
            "National contexts differ (EU vs US vs APAC).",
        ],
        "recap": [
            "Industry readiness is uneven but improving.",
            "PQC and talent are common gaps.",
            "Supervisors want measured experimentation, not hype.",
        ],
        "next_steps": [
            "Read FCA 2024 regulatory paper.",
            "Draft a one-page readiness checklist for a fictional bank.",
            "Explore PQC roadmap tutorial.",
        ],
        "imports_extra": """import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _common import savefig""",
        "demo_fn": '''def run_demo() -> None:
    """Simulate readiness scores across four pillars."""
    pillars = ["Talent", "Strategy", "Infrastructure", "PQC prep"]
    scores_2023 = np.array([0.35, 0.40, 0.30, 0.25])
    scores_2025 = np.array([0.50, 0.55, 0.45, 0.48])
    explain("Illustrative industry readiness (0–1) from survey-style data.")
    for p, s0, s1 in zip(pillars, scores_2023, scores_2025):
        print(f"  {p:16s} | 2023={s0:.2f} -> 2025={s1:.2f} (+{s1-s0:.2f})")
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.arange(len(pillars))
    ax.bar(x - 0.2, scores_2023, 0.4, label="2023")
    ax.bar(x + 0.2, scores_2025, 0.4, label="2025")
    ax.set_xticks(x, pillars, rotation=15)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Readiness score")
    ax.set_title("Bank of Finland-style readiness pillars")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    path = savefig(fig, __file__, "bof_readiness.png")
    plt.close(fig)
    print(f"\\n  Plot saved to: {path}")''',
    },
    "L2A_01_jpmorgan_decomposition_2025": {
        "subtitle": "Decomposition pipeline for large-scale portfolio optimization",
        "finance_problem": [
            "Real portfolios may have thousands of assets. A monolithic QUBO is too "
            "large for current quantum hardware.",
            "JPMorgan proposes decomposing the problem into smaller blocks solved "
            "hybridly and reassembled.",
        ],
        "paper_idea": [
            "Use clustering or graph partitioning on the covariance structure, solve "
            "sub-QUBOs on quantum/annealing devices, then coordinate classically.",
        ],
        "concepts": [
            ("Block decomposition", "Splitting a large problem into manageable subproblems."),
            ("Coupling matrix", "Covariance or constraint links between assets."),
            ("Hybrid coordinator", "Classical layer that merges sub-solutions and enforces global constraints."),
        ],
        "analogy": "Like solving a giant jigsaw by working on corners and color clusters first, then fitting them together.",
        "limitations": [
            "Decomposition can sacrifice global optimality.",
            "Interface constraints between blocks need careful tuning.",
            "Still needs classical heavy lifting for data and validation.",
        ],
        "recap": [
            "Scale is the main obstacle for quantum portfolio opt.",
            "Decomposition is a practical engineering strategy.",
            "JPMorgan pipeline targets institution-sized universes.",
        ],
        "next_steps": [
            "Try BBVA VQE tutorial for dynamic constraints.",
            "Run quantum/tesi/03_portfolio_optimization_qubo.py.",
            "Read IonQ 2026 large-scale demo paper.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Partition a 6-asset covariance matrix into two QUBO blocks."""
    rng = np.random.default_rng(11)
    n = 6
    A = rng.standard_normal((n, n))
    cov = A @ A.T
    block_a = cov[:3, :3]
    block_b = cov[3:, 3:]
    explain("Toy 6-asset universe split into two 3-asset blocks.")
    print("  Block A diagonal (variances):", np.round(np.diag(block_a), 4))
    print("  Block B diagonal (variances):", np.round(np.diag(block_b), 4))
    cross = cov[:3, 3:]
    print("  Cross-block coupling Frobenius norm:", float(np.linalg.norm(cross, "fro")))''',
    },
    "L2A_02_bbva_vqe_2025": {
        "subtitle": "Scaling VQE for dynamic portfolio optimization",
        "finance_problem": [
            "Portfolios change with market conditions, transaction costs, and "
            "regulatory limits. Static solutions decay quickly.",
        ],
        "paper_idea": [
            "BBVA and IBM study VQE for dynamic portfolio problems with constraints, "
            "testing parameter transfer and circuit depth on hardware.",
        ],
        "concepts": [
            ("VQE", "Variational Quantum Eigensolver minimizes energy of a Hamiltonian encoding the objective."),
            ("Parameter transfer", "Warm-starting VQE from previous day's solution."),
            ("Constraint penalty", "Encoding limits as penalty terms in the Hamiltonian."),
        ],
        "analogy": "VQE is tuning a radio antenna: small knob turns (parameters) until the signal (portfolio cost) is strongest.",
        "limitations": [
            "Barren plateaus and noise hurt convergence.",
            "Dynamic constraints increase circuit complexity.",
            "Beat classical heuristics only on selected instances.",
        ],
        "recap": [
            "VQE is a flagship hybrid approach for portfolio opt.",
            "Dynamic rebalancing needs warm-start strategies.",
            "BBVA work bridges bank requirements and IBM hardware.",
        ],
        "next_steps": [
            "Compare annealing e2e paper L2A_05.",
            "Study PO-QA unified framework.",
            "Encode a 2-asset QUBO manually in the demo.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Brute-force minimize a 2-asset QUBO for three risk-aversion values."""
    mu = np.array([0.12, 0.08])
    cov = np.array([[0.04, 0.01], [0.01, 0.02]])
    lambdas = [0.5, 1.0, 2.0]
    explain("Search binary inclusion x in {0,1}^2 minimizing mu^T x + lambda x^T cov x.")
    for lam in lambdas:
        best_e, best_x = np.inf, None
        for x0 in (0, 1):
            for x1 in (0, 1):
                x = np.array([x0, x1], dtype=float)
                e = mu @ x + lam * x @ cov @ x
                if e < best_e:
                    best_e, best_x = e, x
        print(f"  lambda={lam:.1f} -> x={best_x.astype(int)} energy={best_e:.4f}")''',
    },
    "L2A_03_hybrid_discretization_2025": {
        "subtitle": "Hybrid classical-quantum portfolio opt with discretized weights",
        "finance_problem": [
            "Continuous portfolio weights must be discretized for QUBO encodings. "
            "Too few levels lose precision; too many blow up qubit count.",
        ],
        "paper_idea": [
            "Hybrid pipeline: classical search over coarse grids, quantum solver for "
            "combinatorial subproblems, iterative refinement of discretization.",
        ],
        "concepts": [
            ("Discretization", "Mapping continuous weights to finite bit strings."),
            ("Hybrid loop", "Alternating classical refinement and quantum solve."),
            ("Precision-qubit tradeoff", "More bits per asset increases problem size exponentially."),
        ],
        "analogy": "Like approximating a smooth curve with step sizes—you refine the steps where the curve bends most (active assets).",
        "limitations": [
            "Discretization gap vs continuous optimum.",
            "Multiple passes increase total runtime.",
            "Hardware limits cap bits per asset.",
        ],
        "recap": [
            "Discretization is unavoidable for QUBO portfolios.",
            "Hybrid refinement mitigates coarse grids.",
            "Track gap to continuous classical solution.",
        ],
        "next_steps": [
            "Read JPMorgan decomposition for scaling.",
            "Run annealing e2e tutorial.",
            "Try 3-level weight encoding on paper.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Compare 2-bit vs 3-bit weight grids for one asset (toy)."""
    levels2 = np.array([0.0, 0.33, 0.67, 1.0])
    levels3 = np.array([i / 7 for i in range(8)])
    target = 0.55
    w2 = levels2[np.argmin(np.abs(levels2 - target))]
    w3 = levels3[np.argmin(np.abs(levels3 - target))]
    explain(f"Target weight {target:.2f} on a single asset slot.")
    print(f"  2-bit grid nearest: {w2:.4f} (error {abs(w2-target):.4f})")
    print(f"  3-bit grid nearest: {w3:.4f} (error {abs(w3-target):.4f})")
    print(f"  Qubit cost: 2-bit needs 2 qubits/asset; 3-bit needs 3 qubits/asset.")''',
    },
    "L2A_04_poqa_framework_2024": {
        "subtitle": "PO-QA unified framework for quantum portfolio algorithms",
        "finance_problem": [
            "Teams face a maze of QAOA, VQE, annealing, and hybrid variants without "
            "a common interface to compare them fairly.",
        ],
        "paper_idea": [
            "PO-QA proposes a unified formulation: encode portfolio problems once, "
            "plug in different quantum solvers, standardize metrics and benchmarks.",
        ],
        "concepts": [
            ("QAOA", "Quantum Approximate Optimization Algorithm alternates cost and mixer layers."),
            ("Solver adapter", "Common API wrapping distinct quantum backends."),
            ("Benchmark suite", "Shared instances and KPIs (Sharpe, turnover, runtime)."),
        ],
        "analogy": "PO-QA is USB-C for portfolio solvers—one plug shape, many devices.",
        "limitations": [
            "Framework overhead may hide solver-specific tricks.",
            "Fair tuning budget across solvers is debatable.",
            "Still early for production risk systems.",
        ],
        "recap": [
            "Unification helps reproducible comparisons.",
            "Encode once, swap quantum backend.",
            "PO-QA is methodological glue for L2A papers.",
        ],
        "next_steps": [
            "Run annealing vs QAOA toy demo below.",
            "Pick two papers and compare via PO-QA lens.",
            "Document KPIs before benchmarking.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Same QUBO, two solver scores (QAOA vs annealing) on 3-asset toy."""
    mu = np.array([0.10, 0.07, 0.05])
    Q = np.diag([0.03, 0.02, 0.015])
    best = []
    for x0 in (0, 1):
        for x1 in (0, 1):
            for x2 in (0, 1):
                x = np.array([x0, x1, x2], dtype=float)
                e = mu @ x + x @ Q @ x
                best.append((e, x))
    best.sort(key=lambda t: t[0])
    e_opt, x_opt = best[0]
    qaoa_score = e_opt * 1.05  # noisy solver
    anneal_score = e_opt * 1.02
    explain("Optimal energy vs illustrative QAOA/annealer outputs on same instance.")
    print(f"  optimum x={x_opt.astype(int)} energy={e_opt:.4f}")
    print(f"  QAOA reported energy={qaoa_score:.4f} (gap {(qaoa_score/e_opt-1)*100:.1f}%)")
    print(f"  Annealer reported energy={anneal_score:.4f} (gap {(anneal_score/e_opt-1)*100:.1f}%)")''',
    },
    "L2A_05_annealing_e2e_2025": {
        "subtitle": "End-to-end portfolio optimization with quantum annealing",
        "finance_problem": [
            "Institutions want a full pipeline from market data to tradable weights "
            "using quantum annealers (e.g. D-Wave) as solvers.",
        ],
        "paper_idea": [
            "Authors present QUBO derivation, embedding on annealing hardware, "
            "and classical validation of returned bitstrings.",
        ],
        "concepts": [
            ("Quantum annealing", "Hardware finds low-energy states of an Ising/QUBO problem."),
            ("Minor embedding", "Mapping logical qubits to physical couplers on the chip."),
            ("Chain breaks", "Embedding artifacts that degrade solution quality."),
        ],
        "analogy": "Annealing is rolling a ball through a hilly landscape until it settles in the lowest valley (minimum energy).",
        "limitations": [
            "Limited connectivity on hardware graphs.",
            "Energy scale calibration is tricky.",
            "Competitive vs CPLEX/Gurobi on many instances.",
        ],
        "recap": [
            "Annealing offers real hardware today for QUBOs.",
            "End-to-end means data, QUBO, embed, decode, validate.",
            "Check feasibility of returned portfolios.",
        ],
        "next_steps": [
            "Run quantum/tesi/03_portfolio_optimization_qubo.py.",
            "Compare IonQ gate-based large-scale paper.",
            "Study JPMorgan decomposition for size limits.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Simulated annealing on a 4-asset QUBO (toy e2e energy descent)."""
    mu = np.array([0.11, 0.09, 0.07, 0.06])
    Q = np.diag([0.025, 0.02, 0.018, 0.015])
    rng = np.random.default_rng(3)
    x = rng.integers(0, 2, size=4).astype(float)
    def energy(v):
        return float(mu @ v + v @ Q @ v)
    T = 1.0
    e = energy(x)
    explain("Start from random bitstring and cool temperature.")
    for step in range(8):
        i = rng.integers(0, 4)
        trial = x.copy()
        trial[i] = 1 - trial[i]
        et = energy(trial)
        if et < e or rng.random() < np.exp(-(et - e) / T):
            x, e = trial, et
        T *= 0.7
        print(f"  step {step+1}: x={x.astype(int)} energy={e:.4f} T={T:.3f}")
    print(f"\\n  Final portfolio energy={e:.4f}")''',
    },
    "L2A_06_ionq_large_scale_2026": {
        "subtitle": "Large-scale portfolio optimization on trapped-ion hardware",
        "finance_problem": [
            "Gate-based machines are improving qubit counts and connectivity. "
            "Can they run portfolio instances beyond toy size?",
        ],
        "paper_idea": [
            "IonQ 2026 demonstration scales portfolio QUBO instances on trapped-ion "
            "devices, reporting solution quality vs classical heuristics.",
        ],
        "concepts": [
            ("Trapped-ion QC", "Qubits stored in ions manipulated by lasers; often high fidelity."),
            ("Circuit depth", "Number of gate layers; affects noise accumulation."),
            ("Solution quality", "Objective value vs best known classical baseline."),
        ],
        "analogy": "Scaling qubits is like expanding an orchestra—more musicians only help if they stay in time (low noise).",
        "limitations": [
            "Queue times and cost for cloud access.",
            "Instance sizes still below daily production universes.",
            "Fair classical tuning may narrow reported gaps.",
        ],
        "recap": [
            "Hardware demos prove growing capability.",
            "Compare fairly against strong classical baselines.",
            "IonQ paper anchors gate-based portfolio scaling.",
        ],
        "next_steps": [
            "Read JPMorgan decomposition for when hardware is still too small.",
            "Track circuit depth vs error in L3 thesis tutorials.",
            "Benchmark your own QUBO on cloud IonQ if available.",
        ],
        "imports_extra": """import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _common import savefig""",
        "demo_fn": '''def run_demo() -> None:
    """Project solution quality vs number of assets (toy scaling curve)."""
    assets = np.array([4, 8, 16, 32, 64])
    classical_gap = 0.02 * np.log(assets)  # % above best
    ionq_gap = 0.05 + 0.03 * np.log(assets)
    explain("Gap to best-known objective (lower is better) — illustrative only.")
    for a, cg, ig in zip(assets, classical_gap, ionq_gap):
        print(f"  n={a:2d} assets | classical heuristic gap={cg*100:.1f}% | ionq demo gap={ig*100:.1f}%")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(assets, classical_gap * 100, "o-", label="Classical heuristic")
    ax.plot(assets, ionq_gap * 100, "s-", label="Trapped-ion demo")
    ax.set_xlabel("Number of assets")
    ax.set_ylabel("Optimality gap (%)")
    ax.set_title("Large-scale portfolio scaling (toy)")
    ax.legend()
    ax.grid(alpha=0.3)
    path = savefig(fig, __file__, "ionq_scaling.png")
    plt.close(fig)
    print(f"\\n  Plot saved to: {path}")''',
    },
    "L2B_01_stamatopoulos_options_2020": {
        "subtitle": "Option pricing using quantum computers (JPMorgan)",
        "finance_problem": [
            "European and path-dependent options under stochastic volatility models "
            "require many Monte Carlo paths for tight confidence intervals.",
        ],
        "paper_idea": [
            "Stamatopoulos et al. detail a quantum pipeline for European options: "
            "state preparation, payoff oracle, and QAE for price estimation.",
        ],
        "concepts": [
            ("GBM", "Geometric Brownian Motion baseline for equity underlyings."),
            ("Payoff oracle", "Quantum circuit marking paths with positive option payoff."),
            ("Price from amplitude", "Option price linked to estimated payoff probability/amplitude."),
        ],
        "analogy": "QAE option pricing counts winning lottery tickets (ITM paths) with fewer draws than classical sampling.",
        "limitations": [
            "Log-normal assumptions break in crises.",
            "Oracle construction for exotic payoffs is hard.",
            "Practical speedup not yet demonstrated at bank scale.",
        ],
        "recap": [
            "Stamatopoulos is the canonical bank option + QAE reference.",
            "Classical MC remains the production baseline.",
            "QAE targets the statistical error bottleneck.",
        ],
        "next_steps": [
            "Run quantum/tesi/02_european_option_monte_carlo.py.",
            "Read Jauron thesis tutorial L3_01.",
            "Study Rebentrost MC 2018 foundations.",
        ],
        "imports_extra": "from scipy.stats import norm",
        "demo_fn": '''def run_demo() -> None:
    """Price a European call via MC and compare to Black-Scholes."""
    S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
    n = 50_000
    rng = np.random.default_rng(21)
    z = rng.standard_normal(n)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)
    payoffs = np.maximum(ST - K, 0.0)
    mc_price = np.exp(-r * T) * payoffs.mean()
    se = np.exp(-r * T) * payoffs.std(ddof=1) / np.sqrt(n)
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    bs = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    explain("Toy Stamatopoulos baseline: MC vs analytic Black-Scholes.")
    print(f"  MC price = {mc_price:.4f} +/- {1.96*se:.4f} (95% CI)")
    print(f"  Black-Scholes = {bs:.4f}")
    print(f"  ITM probability estimate = {(payoffs > 0).mean():.4f}")''',
    },
    "L2B_02_goldman_market_risk_2022": {
        "subtitle": "Towards quantum advantage in financial market risk",
        "finance_problem": [
            "Market risk engines compute VaR and CVaR under many scenarios. "
            "Tight tails need enormous scenario counts.",
        ],
        "paper_idea": [
            "Goldman analyzes resource requirements for quantum acceleration of "
            "risk metrics, comparing qubit counts and depths to classical clusters.",
        ],
        "concepts": [
            ("VaR", "Value at Risk: loss threshold at a confidence level."),
            ("CVaR", "Expected shortfall beyond the VaR threshold."),
            ("Scenario generation", "Simulating correlated market factors."),
        ],
        "analogy": "Risk engines are weather models for losses—quantum aims to forecast rare storms with fewer simulations.",
        "limitations": [
            "Regulatory approval for quantum risk models is untested.",
            "Data governance limits cloud quantum use.",
            "Constant-factor overheads may dominate asymptotic gains.",
        ],
        "recap": [
            "Goldman quantifies what 'advantage' might mean for risk.",
            "Tail metrics are the hardest and most interesting target.",
            "Resource estimates guide multi-year R&D planning.",
        ],
        "next_steps": [
            "Run L2B_03_qmc_risk_2024 tutorial.",
            "Try VaR demo below with more scenarios.",
            "Read counterparty credit risk 2025 paper.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Estimate 95% VaR from linear P&L scenarios."""
    rng = np.random.default_rng(9)
    n = 20_000
    factors = rng.standard_normal((n, 3))
    weights = np.array([0.4, -0.2, 0.1])
    pnl = factors @ weights
    var_95 = -np.quantile(pnl, 0.05)
    explain("Linear toy P&L from three risk factors; 95% VaR as 5th percentile loss.")
    print(f"  scenarios = {n}")
    print(f"  95% VaR (loss positive) = {var_95:.4f}")
    print(f"  worst 1% mean (CVaR proxy) = {-pnl[pnl <= np.quantile(pnl, 0.01)].mean():.4f}")''',
    },
    "L2B_03_qmc_risk_2024": {
        "subtitle": "Quantum Monte Carlo for financial risk analytics",
        "finance_problem": [
            "Risk teams need end-to-end pipelines producing VaR, CVaR, and stress "
            "metrics under tight latency budgets.",
        ],
        "paper_idea": [
            "2024 QMC work describes integrating quantum subroutines for tail "
            "probability estimation inside risk analytics stacks.",
        ],
        "concepts": [
            ("Tail probability", "Rare-event frequency driving VaR/CVaR."),
            ("QMC pipeline", "Data ingest -> scenario gen -> quantum estimate -> validation."),
            ("Backtesting", "Checking VaR exceptions on historical data."),
        ],
        "analogy": "QMC risk is replacing the slowest gear in a watch—the tail estimator—while keeping the case and dial classical.",
        "limitations": [
            "Production risk systems are heavily regulated and validated.",
            "Quantum modules must pass same backtesting as classical.",
            "End-to-end advantage unproven on real books.",
        ],
        "recap": [
            "Focus on tail metrics where MC is expensive.",
            "Pipeline thinking beats isolated circuit demos.",
            "Validation and governance are as hard as physics.",
        ],
        "next_steps": [
            "Extend Goldman resource estimates with your book size.",
            "Run counterparty credit tutorial.",
            "Practice backtesting VaR on historical series.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Compare MC vs ideal QAE queries for tail probability p=0.05."""
    p = 0.05
    eps = 0.005
    classical_n = int(np.ceil(1 / eps**2))
    qae_n = int(np.ceil(1 / eps))
    explain(f"Target tail probability p={p}, precision eps={eps}.")
    print(f"  classical samples ~ O(1/eps^2) = {classical_n}")
    print(f"  ideal QAE queries ~ O(1/eps) = {qae_n}")
    print(f"  ratio classical/QAE ~ {classical_n/qae_n:.1f}x")''',
    },
    "L2B_04_counterparty_credit_2025": {
        "subtitle": "Quantum counterparty credit risk for path-dependent derivatives",
        "finance_problem": [
            "Counterparty exposure on path-dependent trades depends on many future "
            "market paths and netting sets—expensive to simulate classically.",
        ],
        "paper_idea": [
            "Authors explore quantum acceleration for exposure profiles and CVA-like "
            "metrics on path-dependent structures.",
        ],
        "concepts": [
            ("Exposure profile", "Expected positive exposure over time buckets."),
            ("CVA", "Credit Valuation Adjustment: price of counterparty default risk."),
            ("Path dependence", "Payoff depends on entire trajectory, not just terminal price."),
        ],
        "analogy": "Counterparty risk is measuring how much rope you lent out on a windy day—paths matter, not just the final position.",
        "limitations": [
            "Netting and collateral rules complicate oracles.",
            "Legal and data heterogeneity across desks.",
            "Quantum advantage unproven with real netting sets.",
        ],
        "recap": [
            "Path-dependent exposure is a natural MC target.",
            "Quantum aims at scenario count reduction.",
            "Credit risk integration is harder than single-name options.",
        ],
        "next_steps": [
            "Review Stamatopoulos option pricing baseline.",
            "Simulate exposure profiles classically first.",
            "Read Goldman market risk for resource context.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Toy positive exposure on a capped payoff path."""
    rng = np.random.default_rng(5)
    n_paths, steps = 5000, 12
    paths = np.cumsum(rng.standard_normal((n_paths, steps)) * 0.01, axis=1)
    payoff = np.maximum(paths.max(axis=1) - 1.02, 0.0)
    exposure = payoff.mean()
    explain("Max-path trigger exposure (illustrative path-dependent structure).")
    print(f"  paths={n_paths}, steps={steps}")
    print(f"  mean positive exposure metric = {exposure:.6f}")
    print(f"  95th percentile exposure = {np.quantile(payoff, 0.95):.6f}")''',
    },
    "L2C_01_fraud_qgnn_2024": {
        "subtitle": "Financial fraud detection using quantum graph neural networks",
        "finance_problem": [
            "Fraud rings hide in transaction graphs. Classical GNNs work but may "
            "struggle with certain feature maps at scale.",
        ],
        "paper_idea": [
            "Innan 2024 proposes QGNN layers: quantum circuits process graph "
            "adjacency and node features for classification of fraudulent nodes.",
        ],
        "concepts": [
            ("GNN", "Neural network that propagates information along graph edges."),
            ("QGNN", "Quantum layers replace or augment linear message passing."),
            ("Imbalanced data", "Fraud is rare; metrics must handle class imbalance."),
        ],
        "analogy": "A QGNN is a metal detector tuned for hidden connections in a subway map of payments.",
        "limitations": [
            "Real graphs are huge and privacy-sensitive.",
            "Quantum advantage not proven on production fraud data.",
            "Explainability requirements in banking are strict.",
        ],
        "recap": [
            "Graph structure is key for fraud.",
            "QGNNs are exploratory but promising for pattern richness.",
            "Always compare to strong classical GNN baselines.",
        ],
        "next_steps": [
            "Read QML finance surveys L1_01 and Doosti.",
            "Try classical graph features before quantum layers.",
            "Study class imbalance handling (precision-recall).",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Toy graph: adjacency matrix and one-hop neighbor feature average."""
    A = np.array([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]], dtype=float)
    features = np.array([0.1, 0.8, 0.3, 0.9])
    deg = A.sum(axis=1, keepdims=True)
    deg[deg == 0] = 1
    agg = (A @ features) / deg.ravel()
    explain("Node features aggregated from neighbors (classical GNN step).")
    for i, (f, a) in enumerate(zip(features, agg)):
        label = "suspicious" if a > 0.5 and f > 0.5 else "ok"
        print(f"  node {i}: feature={f:.2f} neighbor_avg={a:.2f} -> {label}")''',
    },
    "L2D_01_pqc_roadmap_2025": {
        "subtitle": "Global roadmaps for post-quantum era in finance",
        "finance_problem": [
            "Financial infrastructure relies on RSA/ECC for TLS, signing, and "
            "key exchange. Quantum threatens these primitives.",
        ],
        "paper_idea": [
            "MDPI 2025 reviews NIST PQC standards, migration waves, and finance-specific "
            "timelines for HSM upgrades, PKI, and third-party vendors.",
        ],
        "concepts": [
            ("PQC", "Cryptography safe against known quantum attacks."),
            ("Crypto agility", "Ability to swap algorithms without rewiring entire systems."),
            ("Harvest now decrypt later", "Adversaries store ciphertext for future decryption."),
        ],
        "analogy": "PQC migration is changing every lock in a skyscraper while people still work inside—plan carefully.",
        "limitations": [
            "Standards still stabilizing; hybrid modes add complexity.",
            "Legacy mainframes are slow to upgrade.",
            "Vendor chains multiply coordination cost.",
        ],
        "recap": [
            "PQC is more urgent than quantum portfolio pilots for many banks.",
            "Inventory crypto usage before buying quantum compute time.",
            "Roadmaps differ by jurisdiction but direction is clear.",
        ],
        "next_steps": [
            "Read FCA 2024 regulatory discussion.",
            "List TLS and signing algorithms in a sample architecture.",
            "Follow NIST ML-KEM / ML-DSA standard docs.",
        ],
        "imports_extra": "",
        "demo_fn": '''def run_demo() -> None:
    """Toy migration waves for finance systems."""
    systems = ["Mobile app TLS", "HSM signing", "Interbank SWIFT", "Archive DB"]
    years = np.array([2025, 2026, 2027, 2029])
    risk = np.array([0.9, 0.95, 0.85, 0.7])
    explain("Planned PQC migration year vs residual classical risk (toy).")
    for s, y, r in zip(systems, years, risk):
        print(f"  {s:18s} | migrate by {y} | residual risk score {r:.2f}")''',
    },
    "L3_01_jauron_thesis_2022": {
        "subtitle": "Master's thesis — pricing options on quantum computers",
        "finance_problem": [
            "Thesis work needs a reproducible pipeline from payoff definition to "
            "quantum circuit metrics and error analysis.",
        ],
        "paper_idea": [
            "Jauron (Sherbrooke, 2022) implements European option pricing with QAE, "
            "documenting circuits, simulations, and hardware considerations.",
        ],
        "concepts": [
            ("Thesis workflow", "Problem -> classical baseline -> quantum design -> evaluation."),
            ("Circuit depth", "Gate count layers affecting noise sensitivity."),
            ("Simulation vs hardware", "Ideal simulators vs noisy device results."),
        ],
        "analogy": "A thesis is a lab notebook with receipts—every claim tied to a script, circuit, or plot.",
        "limitations": [
            "Thesis instances are smaller than production books.",
            "Hardware results age as devices improve.",
            "Some steps rely on simulators only.",
        ],
        "recap": [
            "Jauron is a reference implementation narrative.",
            "Always anchor to classical MC/BS prices.",
            "Document depth, shots, and error bars.",
        ],
        "next_steps": [
            "Read Berube 2024 thesis for improvements.",
            "Run quantum/tesi/02_european_option_monte_carlo.py.",
            "Reproduce payoff oracle on paper for 1-qubit toy.",
        ],
        "imports_extra": "from scipy.stats import norm",
        "demo_fn": '''def run_demo() -> None:
    """Thesis-style checklist metrics for a European call run."""
    S0, K, r, sigma, T = 100, 105, 0.03, 0.25, 0.5
    d1 = (np.log(S0/K) + (r+0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    bs = S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    steps = ["Define payoff", "Build oracle", "Run QAE", "Compare to BS"]
    explain("Workflow steps with final Black-Scholes reference.")
    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")
    print(f"\\n  Black-Scholes call price = {bs:.4f}")
    print(f"  Target MC stderr ~ 0.01 needs ~{(1.96/0.01)**2 * 0.25:.0f} paths (rough)")''',
    },
    "L3_02_berube_thesis_2024": {
        "subtitle": "Extended thesis — improved circuits and benchmarks",
        "finance_problem": [
            "Earlier thesis results may use deep circuits or optimistic assumptions. "
            "Berube 2024 refines circuits and benchmarks against updated hardware.",
        ],
        "paper_idea": [
            "Improved state preparation, reduced depth, and systematic comparison "
            "to Jauron 2022 and classical baselines on larger instances.",
        ],
        "concepts": [
            ("Depth reduction", "Fewer gates means less noise accumulation."),
            ("Benchmark harness", "Scripts that replay experiments with fixed seeds."),
            ("Error mitigation", "Post-processing to reduce bias from noise."),
        ],
        "analogy": "Berube is the director's cut—same story, tighter editing and better camera (circuits).",
        "limitations": [
            "Still academic scale.",
            "Mitigation tricks may not generalize.",
            "Rapid hardware changes outdate specific numbers.",
        ],
        "recap": [
            "Second thesis iterates on circuit efficiency.",
            "Compare fairly with fixed shot budgets.",
            "Treat depth as a first-class KPI.",
        ],
        "next_steps": [
            "Diff Berube vs Jauron workflow tables.",
            "Profile depth vs accuracy tradeoff in demo.",
            "Read Stamatopoulos industry paper for context.",
        ],
        "imports_extra": """import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _common import savefig""",
        "demo_fn": '''def run_demo() -> None:
    """Depth vs error tradeoff (toy model of thesis benchmark)."""
    depth = np.array([10, 20, 40, 80, 160])
    err_jauron = 0.02 + 0.0008 * depth
    err_berube = 0.02 + 0.0004 * depth
    explain("Illustrative pricing error vs circuit depth for two thesis generations.")
    for d, e1, e2 in zip(depth, err_jauron, err_berube):
        print(f"  depth={d:3d} | Jauron err={e1:.4f} | Berube err={e2:.4f}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(depth, err_jauron, "o-", label="Jauron 2022 (toy)")
    ax.plot(depth, err_berube, "s-", label="Berube 2024 (toy)")
    ax.set_xlabel("Circuit depth")
    ax.set_ylabel("Pricing error")
    ax.set_title("Thesis benchmark: depth vs error")
    ax.legend()
    ax.grid(alpha=0.3)
    path = savefig(fig, __file__, "thesis_depth_error.png")
    plt.close(fig)
    print(f"\\n  Plot saved to: {path}")''',
    },
}


def _lit(s: str) -> str:
    """Safe Python string literal for generated source."""
    return repr(s)


def _py_string_list(items: list[str], indent: int = 8) -> str:
    pad = " " * indent
    return "\n".join(f"{pad}{_lit(s)}," for s in items)


def _py_concepts(items: list[tuple[str, str]], indent: int = 8) -> str:
    pad = " " * indent
    return "\n".join(f"{pad}({_lit(a)}, {_lit(b)})," for a, b in items)


def render_script(
    slug: str,
    folder: str,
    title: str,
    objective: str,
    arxiv: str,
    level_id: str,
    level_title: str,
    content: dict[str, Any],
) -> str:
    rel_path = f"quantum/tesi/papers/{folder}/{slug}.py"
    imports_extra = content.get("imports_extra", "").strip()
    extra_import_block = f"{imports_extra}\n\n" if imports_extra else ""
    level_label = f"{level_id} — {level_title}"

    return f'''"""
Tutorial — {title}
Slug: {slug}
Level: {level_label}

Run from repo root:
    python {rel_path}
"""
from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parents[2]))  # quantum/
sys.path.insert(0, str(_SCRIPT_DIR.parents[1]))  # quantum/tesi/

import numpy as np
{extra_import_block}from _lib.beginner import (
    analogy,
    banner,
    concept_box,
    explain,
    next_steps,
    paper_info,
    recap,
    section,
)

{content["demo_fn"]}


def main() -> None:
    banner({_lit(title)}, {_lit(content["subtitle"])})
    paper_info(
        {_lit(title)},
        {_lit(objective)},
        arxiv={_lit(arxiv)},
        level={_lit(level_label)},
    )

    section(1, "The Finance Problem")
    explain(
{_py_string_list(content["finance_problem"])}
    )

    section(2, "What the Paper Proposes")
    explain(
{_py_string_list(content["paper_idea"])}
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
{_py_concepts(content["concepts"])}
        ]
    )
    analogy({_lit(content["analogy"])})

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
{_py_string_list(content["limitations"])}
    )

    section(6, "Recap")
    recap(
        [
{_py_string_list(content["recap"])}
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
{_py_string_list(content["next_steps"])}
        ]
    )


if __name__ == "__main__":
    main()
'''


def load_catalog_entries() -> list[dict[str, Any]]:
    with CATALOG_PATH.open(encoding="utf-8") as f:
        catalog = yaml.safe_load(f)
    entries: list[dict[str, Any]] = []
    for level in catalog["levels"]:
        for paper in level["papers"]:
            entries.append(
                {
                    "level_id": level["id"],
                    "level_title": level["title"],
                    "folder": FOLDER_MAP[level["id"]],
                    "title": paper["title"],
                    "objective": paper["objective"],
                    "arxiv": paper.get("arxiv", ""),
                }
            )
    return entries


def generate_all() -> list[Path]:
    if len(SLUG_ORDER) != 25:
        raise ValueError(f"Expected 25 slugs, got {len(SLUG_ORDER)}")
    entries = load_catalog_entries()
    if len(entries) != 25:
        raise ValueError(f"Expected 25 catalog papers, got {len(entries)}")

    created: list[Path] = []
    for (level_id, slug), meta in zip(SLUG_ORDER, entries):
        if slug not in PAPERS:
            raise KeyError(f"Missing PAPERS content for {slug}")
        if meta["level_id"] != level_id:
            raise ValueError(f"Level mismatch for {slug}: catalog {meta['level_id']} vs {level_id}")

        folder = FOLDER_MAP[level_id]
        out_dir = PAPERS_DIR / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{slug}.py"
        script = render_script(
            slug=slug,
            folder=folder,
            title=meta["title"],
            objective=meta["objective"],
            arxiv=meta["arxiv"],
            level_id=meta["level_id"],
            level_title=meta["level_title"],
            content=PAPERS[slug],
        )
        out_path.write_text(script, encoding="utf-8")
        created.append(out_path)
    return created


def generate_readme(created: list[Path]) -> Path:
    entries = load_catalog_entries()
    rows: list[str] = [
        "# Paper tutorials index",
        "",
        "Beginner-friendly runnable tutorials generated from `papers_catalog.yaml`.",
        "",
        "Regenerate:",
        "```bash",
        "python quantum/tesi/materialize_paper_tutorials.py",
        "```",
        "",
        "| Slug | Paper | Run command |",
        "|------|-------|-------------|",
    ]
    for (level_id, slug), meta in zip(SLUG_ORDER, entries):
        folder = FOLDER_MAP[level_id]
        cmd = f"python quantum/tesi/papers/{folder}/{slug}.py"
        link = f"https://arxiv.org/abs/{meta['arxiv']}" if meta["arxiv"] else "—"
        title = meta["title"].replace("|", "\\|")
        rows.append(f"| `{slug}` | {title} | `{cmd}` |")
        if meta["arxiv"]:
            rows[-1] = f"| `{slug}` | [{title}]({link}) | `{cmd}` |"

    readme_path = PAPERS_DIR / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return readme_path


def main() -> None:
    created = generate_all()
    readme = generate_readme(created)
    print(f"Generated {len(created)} tutorials under {PAPERS_DIR}")
    print(f"Index: {readme}")
    for p in created:
        print(f"  - {p.relative_to(ROOT.parents[1])}")


if __name__ == "__main__":
    main()
