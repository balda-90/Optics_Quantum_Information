"""
Tutorial — FCA — Quantum computing in financial services 2024
Slug: L1_02_fca_regulatory_2024
Level: L1 — Industry surveys & policy

Run from repo root:
    python quantum/tesi/papers/L1_survey/L1_02_fca_regulatory_2024.py
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
    """Weighted risk-opportunity index for quantum adoption areas."""
    areas = ["Derivatives pricing", "Portfolio opt", "Fraud ML", "Core banking crypto"]
    opportunity = np.array([0.7, 0.6, 0.5, 0.2])
    risk = np.array([0.4, 0.5, 0.4, 0.9])
    net = opportunity - risk
    explain("Net score = opportunity - risk (toy regulatory lens).")
    for a, o, r, n in zip(areas, opportunity, risk, net):
        print(f"  {a:22s} | opp={o:.1f} risk={r:.1f} | net={n:+.1f}")
    print(f"\n  Highest priority concern: {areas[int(np.argmax(risk))]}")


def main() -> None:
    banner('FCA — Quantum computing in financial services 2024', 'UK FCA view on quantum in financial services')
    paper_info(
        'FCA — Quantum computing in financial services 2024',
        'Regulatory view on opportunities and risks.',
        arxiv='',
        level='L1 — Industry surveys & policy',
    )

    section(1, "The Finance Problem")
    explain(
        'Regulators must balance innovation with market stability, consumer protection, and operational resilience.',
        'Quantum computing brings both opportunity (better models) and threat (breaking classical cryptography).',
    )

    section(2, "What the Paper Proposes")
    explain(
        'The FCA discussion paper frames how firms should assess quantum readiness, third-party risk, and governance for pilot projects.',
        'It highlights post-quantum cryptography migration as a near-term priority.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Operational resilience', 'Ability to continue critical services through technology disruptions.'),
        ('Model risk management', 'Validating that new models (including quantum) are fit for purpose.'),
        ('PQC migration', 'Upgrading crypto systems before large-scale quantum attacks become realistic.'),
        ]
    )
    analogy("The FCA paper is the building inspector's checklist before you install a new power system in a skyscraper bank.")

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'Regulatory guidance evolves; local rules differ by jurisdiction.',
        'Firms may treat quantum as R&D without operational integration plans.',
        'PQC timelines are uncertain but migration is lengthy.',
    )

    section(6, "Recap")
    recap(
        [
        'Regulators see quantum as strategic, not just academic.',
        'Risk management and crypto migration are top themes.',
        'Governance must precede flashy pilots.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Read L2D_01_pqc_roadmap_2025 for migration timelines.',
        'Review Bank of Finland 2025 readiness survey.',
        'Map internal crypto inventory before quantum pilots.',
        ]
    )


if __name__ == "__main__":
    main()
