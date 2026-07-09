"""
Tutorial — Portfolio optimization to quantum blockchain — 2025
Slug: L1_04_portfolio_blockchain_2025
Level: L1 — Industry surveys & policy

Run from repo root:
    python quantum/tesi/papers/L1_survey/L1_04_portfolio_blockchain_2025.py
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
    print(f"  checksum tag for ledger = {checksum}")


def main() -> None:
    banner('Portfolio optimization to quantum blockchain — 2025', 'Survey linking portfolio optimization and quantum blockchain')
    paper_info(
        'Portfolio optimization to quantum blockchain — 2025',
        'Broad survey linking optimization and distributed ledgers.',
        arxiv='',
        level='L1 — Industry surveys & policy',
    )

    section(1, "The Finance Problem")
    explain(
        'Portfolio decisions increasingly interact with tokenized assets and distributed ledgers. Optimization must respect settlement and custody constraints.',
    )

    section(2, "What the Paper Proposes")
    explain(
        'The survey connects quantum optimization methods with blockchain-inspired distributed portfolio governance and smart-contract execution.',
    )

    section(3, "Quantum Concepts for Beginners")
    concept_box(
        [
        ('Tokenized assets', 'On-chain representations of traditional securities.'),
        ('Smart contract', 'Automated rules for rebalancing or collateral management.'),
        ('QUBO on chain', 'Optimization results committed as verifiable on-chain proposals.'),
        ]
    )
    analogy('Quantum optimization proposes the portfolio; blockchain is the notary and automated clerk that records and executes it.')

    section(4, "Hands-On Demo")
    explain(
        "The code below is a small numerical experiment you can run on any laptop.",
        "It is inspired by the paper's theme but simplified for learning.",
    )
    run_demo()

    section(5, "Limitations and Practical Considerations")
    explain(
        'On-chain quantum solvers are not realistic; oracles bridge off-chain compute.',
        'Latency and privacy conflict with transparent ledgers.',
        'Regulatory treatment of tokenized funds varies.',
    )

    section(6, "Recap")
    recap(
        [
        'Optimization and settlement layers should be designed together.',
        'Quantum solvers likely stay off-chain in near term.',
        'Survey papers help spot cross-domain integration risks.',
        ]
    )

    section(7, "Next Steps")
    next_steps(
        [
        'Study PO-QA framework tutorial L2A_04_poqa_framework_2024.',
        'Review BBVA VQE dynamic portfolio paper.',
        'List custody constraints before encoding QUBOs.',
        ]
    )


if __name__ == "__main__":
    main()
