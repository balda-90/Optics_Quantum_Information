"""
Tutorial — Global Roadmaps for Post-Quantum Era in Finance — MDPI 2025
Slug: L2D_01_pqc_roadmap_2025
Level: L2D — Post-quantum cryptography

Run from repo root:
    python quantum/tesi/papers/L2D_pqc/L2D_01_pqc_roadmap_2025.py
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
    """Toy migration waves for finance systems."""
    systems = ["Mobile app TLS", "HSM signing", "Interbank SWIFT", "Archive DB"]
    years = np.array([2025, 2026, 2027, 2029])
    risk = np.array([0.9, 0.95, 0.85, 0.7])
    explain("Planned PQC migration year vs residual classical risk (toy).")
    for s, y, r in zip(systems, years, risk):
        print(f"  {s:18s} | migrate by {y} | residual risk score {r:.2f}")


def main() -> None:
    banner('Global Roadmaps for Post-Quantum Era in Finance — MDPI 2025', 'Global roadmaps for post-quantum era in finance')
    paper_info(
        'Global Roadmaps for Post-Quantum Era in Finance — MDPI 2025',
        'Migration timelines and standards for finance.',
        arxiv='',
        level='L2D — Post-quantum cryptography',
    )

    section(1, "The Finance Problem")
    explain(
        'Financial infrastructure relies on RSA/ECC for TLS, signing, and key exchange. Quantum threatens these primitives.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'MDPI 2025 reviews NIST PQC standards, migration waves, and finance-specific timelines for HSM upgrades, PKI, and third-party vendors.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('PQC', 'Cryptography safe against known quantum attacks.'),
        ('Crypto agility', 'Ability to swap algorithms without rewiring entire systems.'),
        ('Harvest now decrypt later', 'Adversaries store ciphertext for future decryption.'),
        ]
    )
    analogy('PQC migration is changing every lock in a skyscraper while people still work inside—plan carefully.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Standards still stabilizing; hybrid modes add complexity.',
        'Legacy mainframes are slow to upgrade.',
        'Vendor chains multiply coordination cost.',
    )

    section(6, "Recap")
    recap(
        [
        'PQC is more urgent than quantum portfolio pilots for many banks.',
        'Inventory crypto usage before buying quantum compute time.',
        'Roadmaps differ by jurisdiction but direction is clear.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read FCA 2024 regulatory discussion.',
        'List TLS and signing algorithms in a sample architecture.',
        'Follow NIST ML-KEM / ML-DSA standard docs.',
        ]
    )


if __name__ == "__main__":
    main()
