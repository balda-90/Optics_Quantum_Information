"""
Tutorial — Brief review of QML for financial services — Doosti 2024
Slug: L1_05_doosti_qml_review_2024
Level: L1 — Industry surveys & policy

Run from repo root:
    python quantum/tesi/papers/L1_survey/L1_05_doosti_qml_review_2024.py
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
    """Classify finance datasets by suggested QML family."""
    datasets = [
        ("Wire transfer logs", "QSVM / VQC"),
        ("Trader graph", "QGNN"),
        ("Yield curves", "QPCA + regressor"),
    ]
    explain("Toy mapping from data modality to QML family (Doosti-style).")
    for name, fam in datasets:
        print(f"  {name:20s} -> {fam}")


def main() -> None:
    banner('Brief review of QML for financial services — Doosti 2024', 'Compact QML taxonomy for financial services')
    paper_info(
        'Brief review of QML for financial services — Doosti 2024',
        'Compact QML taxonomy for finance.',
        arxiv='2407.12618',
        level='L1 — Industry surveys & policy',
    )

    section(1, "The Finance Problem")
    explain(
        'Financial services teams need a short map of QML algorithms without reading dozens of physics papers.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Doosti 2024 provides a brief taxonomy: supervised/unsupervised QML, kernels, generative models, and finance use-case examples.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('QNN', 'Quantum neural network: layered parameterized circuits.'),
        ('QSVM', 'Quantum support vector machine using quantum feature maps.'),
        ('QPCA', 'Quantum principal component analysis for dimensionality reduction.'),
        ]
    )
    analogy('Doosti is the pocket glossary; the 2024 full QML finance survey is the encyclopedia.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Brief reviews omit implementation detail.',
        'Rapid field growth makes taxonomies incomplete quickly.',
        'Empirical evidence in finance remains limited.',
    )

    section(6, "Recap")
    recap(
        [
        'Taxonomy helps you name and classify QML approaches.',
        'Match algorithm family to data type (tabular, graph, series).',
        'Use as a study guide before thesis-level implementations.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Compare with L1_01_qml_quant_finance_2024.',
        'Run fraud QGNN demo for graph use case.',
        'Pick one algorithm family for a course mini-project.',
        ]
    )


if __name__ == "__main__":
    main()
