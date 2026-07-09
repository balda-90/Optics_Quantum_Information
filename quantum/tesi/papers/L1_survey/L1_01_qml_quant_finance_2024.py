"""
Tutorial — Applications of QML for Quantitative Finance 2024
Slug: L1_01_qml_quant_finance_2024
Level: L1 — Industry surveys & policy

Run from repo root:
    python quantum/tesi/papers/L1_survey/L1_01_qml_quant_finance_2024.py
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
from _lib.beginner import (
    analogy,
    banner,
    concept_box,
    explain,
    next_steps,
    paper_info,
    recap,
    section,
)

def run_demo() -> None:
    """Score QML techniques for three finance tasks (toy rubric)."""
    techniques = ["Quantum kernel SVM", "VQC classifier", "QGAN synthetic data"]
    tasks = ["Credit scoring", "Vol forecasting", "Fraud graphs"]
    scores = np.array([[0.7, 0.5, 0.4], [0.6, 0.6, 0.5], [0.3, 0.4, 0.6]])
    explain("Rubric scores (0–1) for technique-task fit (illustrative).")
    for i, tech in enumerate(techniques):
        best_j = int(np.argmax(scores[i]))
        print(f"  {tech:22s} -> best fit: {tasks[best_j]} ({scores[i, best_j]:.2f})")
    print(f"\n  Mean score per technique: {scores.mean(axis=1)}")


def main() -> None:
    banner('Applications of QML for Quantitative Finance 2024', 'Survey of QML techniques applied to quantitative finance')
    paper_info(
        'Applications of QML for Quantitative Finance 2024',
        'Map QML techniques to quant finance tasks.',
        arxiv='2405.10119',
        level='L1 — Industry surveys & policy',
    )

    section(1, "The Finance Problem")
    explain(
        'Quant teams want to know which QML methods are credible for time-series forecasting, classification, and anomaly detection.',
        'The 2024 survey maps techniques to datasets and evaluation metrics.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Authors categorize QML models (variational classifiers, quantum kernels, QNNs) and align them with finance tasks like volatility forecasting and credit scoring.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Variational classifier', 'Parameterized quantum circuit trained with classical optimizers.'),
        ('Barren plateaus', 'Flat loss landscapes that make training hard at scale.'),
        ('NISQ-friendly QML', "Shallow circuits designed for today's hardware limits."),
        ]
    )
    analogy('This survey is a menu of QML dishes with finance pairing suggestions—not every dish is ready to serve in production.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Benchmarks vary widely; fair comparison to classical ML is hard.',
        'Many studies use pre-quantum-era datasets without market regime shifts.',
        'Regulatory explainability requirements are not always addressed.',
    )

    section(6, "Recap")
    recap(
        [
        'QML in finance spans forecasting, classification, and clustering.',
        'Hardware depth and data encoding dictate feasibility.',
        'Use surveys to shortlist algorithms before deep implementation.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read Doosti 2024 for a shorter taxonomy.',
        'Run L2C_01_fraud_qgnn_2024 hands-on graph demo.',
        'Check FCA 2024 regulatory perspective.',
        ]
    )


if __name__ == "__main__":
    main()
