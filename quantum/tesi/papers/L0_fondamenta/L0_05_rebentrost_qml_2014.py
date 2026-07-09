"""
Tutorial — Quantum algorithms for ML — Rebentrost et al. 2014
Slug: L0_05_rebentrost_qml_2014
Level: L0 — Foundations

Run from repo root:
    python quantum/tesi/papers/L0_fondamenta/L0_05_rebentrost_qml_2014.py
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
    print(f"  angle in feature space = {np.degrees(angle):.2f} degrees")


def main() -> None:
    banner('Quantum algorithms for ML — Rebentrost et al. 2014', 'Quantum algorithms for machine learning foundations')
    paper_info(
        'Quantum algorithms for ML — Rebentrost et al. 2014',
        'HHL-style and distance-based QML building blocks.',
        arxiv='1307.0411',
        level='L0 — Foundations',
    )

    section(1, "The Finance Problem")
    explain(
        'Finance ML tasks include credit scoring, fraud detection, and customer segmentation. Kernel methods and distance metrics are central.',
        'Classical ML on high-dimensional features can be slow at scale.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Rebentrost et al. (2014) present quantum linear algebra tools and distance-based classification ideas (e.g. HHL-related techniques).',
        'They lay groundwork for QML pipelines that finance papers reuse later.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Quantum feature map', 'Encodes classical vectors into quantum states.'),
        ('Kernel', 'A similarity function between data points; quantum circuits can induce kernels.'),
        ('HHL', 'Harrow-Hassidim-Lloyd algorithm for linear systems—promising but resource-heavy.'),
        ]
    )
    analogy('QML feature maps are like translating spreadsheets into a musical score the quantum computer can play—similar data, very different representation.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'HHL needs fault-tolerant resources for practical finance datasets.',
        'Data loading remains O(n) unless structures are exploited.',
        'Many QML demos use tiny synthetic sets only.',
    )

    section(6, "Recap")
    recap(
        [
        'Rebentrost 2014 connects linear algebra and learning on quantum hardware.',
        'Distance/kernel viewpoint links to later fraud and QML surveys.',
        'Not finance-specific, but foundational for L1/L2C papers.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Open L1_01_qml_quant_finance_2024 survey tutorial.',
        'Try L2C_01_fraud_qgnn_2024 for graph-based fraud detection.',
        'Review Doosti 2024 compact QML taxonomy.',
        ]
    )


if __name__ == "__main__":
    main()
