"""
Shared helpers for beginner-friendly paper tutorials.
Every script in quantum/tesi/papers/ uses these to print structured lessons.
"""
from __future__ import annotations

import textwrap
from typing import Iterable


def banner(title: str, subtitle: str = "") -> None:
    line = "=" * 72
    print(f"\n{line}\n  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print(line)


def section(number: int, title: str) -> None:
    print(f"\n{'─' * 72}")
    print(f"  SECTION {number} — {title}")
    print(f"{'─' * 72}")


def explain(*paragraphs: str) -> None:
    for p in paragraphs:
        print(textwrap.fill(p, width=72, subsequent_indent="  "))


def concept_box(items: Iterable[tuple[str, str]]) -> None:
    print("\n  📚 KEY CONCEPTS (beginner)")
    for term, definition in items:
        print(f"\n  • {term}")
        print(textwrap.fill(definition, width=68, initial_indent="    ", subsequent_indent="    "))


def analogy(text: str) -> None:
    print("\n  💡 ANALOGY")
    print(textwrap.fill(text, width=68, initial_indent="    ", subsequent_indent="    "))


def paper_info(title: str, objective: str, arxiv: str = "", level: str = "") -> None:
    print(f"\n  Paper : {title}")
    if level:
        print(f"  Level : {level}")
    if arxiv:
        print(f"  arXiv : https://arxiv.org/abs/{arxiv.replace('arxiv:', '')}")
    print(f"  Goal  : {objective}")


def recap(bullets: Iterable[str]) -> None:
    print("\n  ✅ WHAT YOU SHOULD REMEMBER")
    for b in bullets:
        print(f"    - {b}")


def next_steps(items: Iterable[str]) -> None:
    print("\n  ➡️  NEXT STEPS")
    for i, item in enumerate(items, 1):
        print(f"    {i}. {item}")
