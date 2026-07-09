"""
Tutorial — Financial fraud detection using quantum GNN — Innan 2024
Slug: L2C_01_fraud_qgnn_2024
Level: L2C — Quantum machine learning

Run from repo root:
    python quantum/tesi/papers/L2C_qml/L2C_01_fraud_qgnn_2024.py
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
    """Toy graph: adjacency matrix and one-hop neighbor feature average."""
    A = np.array([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]], dtype=float)
    features = np.array([0.1, 0.8, 0.3, 0.9])
    deg = A.sum(axis=1, keepdims=True)
    deg[deg == 0] = 1
    agg = (A @ features) / deg.ravel()
    explain("Node features aggregated from neighbors (classical GNN step).")
    for i, (f, a) in enumerate(zip(features, agg)):
        label = "suspicious" if a > 0.5 and f > 0.5 else "ok"
        print(f"  node {i}: feature={f:.2f} neighbor_avg={a:.2f} -> {label}")


def main() -> None:
    banner('Financial fraud detection using quantum GNN — Innan 2024', 'Financial fraud detection using quantum graph neural networks')
    paper_info(
        'Financial fraud detection using quantum GNN — Innan 2024',
        'Graph structure + quantum layers for fraud classification.',
        arxiv='2309.01127',
        level='L2C — Quantum machine learning',
    )

    section(1, "The Finance Problem")
    explain(
        'Fraud rings hide in transaction graphs. Classical GNNs work but may struggle with certain feature maps at scale.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'Innan 2024 proposes QGNN layers: quantum circuits process graph adjacency and node features for classification of fraudulent nodes.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('GNN', 'Neural network that propagates information along graph edges.'),
        ('QGNN', 'Quantum layers replace or augment linear message passing.'),
        ('Imbalanced data', 'Fraud is rare; metrics must handle class imbalance.'),
        ]
    )
    analogy('A QGNN is a metal detector tuned for hidden connections in a subway map of payments.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Real graphs are huge and privacy-sensitive.',
        'Quantum advantage not proven on production fraud data.',
        'Explainability requirements in banking are strict.',
    )

    section(6, "Recap")
    recap(
        [
        'Graph structure is key for fraud.',
        'QGNNs are exploratory but promising for pattern richness.',
        'Always compare to strong classical GNN baselines.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read QML finance surveys L1_01 and Doosti.',
        'Try classical graph features before quantum layers.',
        'Study class imbalance handling (precision-recall).',
        ]
    )


if __name__ == "__main__":
    main()
