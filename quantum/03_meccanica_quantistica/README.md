# 03 — Introduzione alla Meccanica Quantistica

Dai postulati (stato, evoluzione, misura) ai fenomeni che non hanno analogo
classico: sovrapposizione ed entanglement. Qui li tocco con mano via circuiti.

## Diario

| Data       | Script                                   | Cosa ho fatto |
|------------|------------------------------------------|---------------|
| 2026-07-04 | `01_stato_di_bell_entanglement.py`       | Costruito lo stato di Bell |Phi+> con H + CNOT su circuito Qiskit + simulatore Aer; disegnato il circuito e misurato le correlazioni (00/11 ~100%). Fallback numpy se Qiskit manca. |

## Prossimi passi
- Disuguaglianza di Bell / test CHSH: violare il limite classico 2.
- I 4 stati di Bell e come distinguerli.
- Teletrasporto quantistico a 3 qubit.

> Girato con Qiskit 2.x + qiskit-aer nel venv dedicato `.venv-quantum`.
