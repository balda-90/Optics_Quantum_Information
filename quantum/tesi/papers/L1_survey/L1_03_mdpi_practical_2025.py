"""
Tutorial — Practical Applications of QC in Finance — MDPI 2025
Slug: L1_03_mdpi_practical_2025
Level: L1 — Industry surveys & policy

Run from repo root:
    python quantum/tesi/papers/L1_survey/L1_03_mdpi_practical_2025.py
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
    """End-to-end latency budget for a hybrid portfolio pilot (toy ms)."""
    stages = ["Data ETL", "QUBO build", "Quantum job", "Decode + validate"]
    classical_ms = np.array([120, 40, 0, 30])
    hybrid_ms = np.array([120, 55, 800, 45])
    explain("Wall-clock breakdown: classical-only vs hybrid cloud job.")
    for s, c, h in zip(stages, classical_ms, hybrid_ms):
        print(f"  {s:16s} | classical {c:4.0f} ms | hybrid {h:4.0f} ms")
    print(f"\n  Total classical: {classical_ms.sum():.0f} ms | hybrid: {hybrid_ms.sum():.0f} ms")


def main() -> None:
    banner('Practical Applications of QC in Finance — MDPI 2025', 'Practitioner-oriented review of QC finance applications')
    paper_info(
        'Practical Applications of QC in Finance — MDPI 2025',
        'Practitioner-oriented application review.',
        arxiv='',
        level='L1 — Industry surveys & policy',
    )

    section(1, "The Finance Problem")
    explain(
        'Practitioners need concrete workflows: data prep, algorithm choice, hardware access, and success metrics—not just asymptotic speedups.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'MDPI 2025 emphasizes practical pipelines for optimization and simulation, including hybrid orchestration and benchmarking against classical stacks.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Hybrid workflow', 'Classical pre/post-processing wrapped around quantum kernels.'),
        ('Benchmarking', 'Measuring wall-clock time, cost, and accuracy—not qubits alone.'),
        ('Vendor stack', 'Cloud quantum access via IBM, IonQ, D-Wave, etc.'),
        ]
    )
    analogy('A practitioner review is the workshop manual; foundational papers are the physics textbook.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Cloud queue times can erase theoretical speedups.',
        'Reproducibility across hardware generations is weak.',
        'Skills gap: few teams know finance and quantum equally well.',
    )

    section(6, "Recap")
    recap(
        [
        'Practical papers focus on end-to-end integration.',
        'Benchmark honestly against your classical production baseline.',
        'Hybrid designs are the default near-term pattern.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Run L2A_05_annealing_e2e_2025 for a full optimization pipeline.',
        'Compare JPMorgan decomposition tutorial.',
        'Document classical baseline before any quantum pilot.',
        ]
    )


if __name__ == "__main__":
    main()
