# Optics & Quantum Information — Coding Journal

Codice sviluppato durante il master in **Ottica e Informazione Quantistica** (Sapienza, Roma).
L'obiettivo è collegare, materia per materia, gli argomenti del corso con il
**quantum computing** attraverso piccoli script eseguibili — uno al giorno, per
costruire un portfolio pubblico e la mia personal brand.

Repo: https://github.com/balda-90/Optics_Quantum_Information

## Struttura

```
quantum/
├── _common/              # utility condivise (algebra, sfera di Bloch, plotting)
├── 01_algebra_calcolo/   # Fondamenti di algebra e calcolo matematico
├── 02_ottica/            # Ottica
├── 03_meccanica_quantistica/  # Introduzione alla Meccanica Quantistica
├── 04_elettronica_quantistica/ # Elettronica quantistica
└── requirements.txt
```

Ogni cartella-materia contiene script numerati (`01_...`, `02_...`) più un
`README.md` che tiene traccia di cosa ho imparato/implementato ogni giorno.

## Setup

Consiglio un ambiente virtuale dedicato a questa parte di codice:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r quantum/requirements.txt
```

> Nota: `numpy`, `scipy` e `matplotlib` bastano per la maggior parte degli script.
> `qiskit` serve solo dove indicato (es. circuiti veri e simulatore Aer). Gli script
> che possono, hanno un fallback in numpy e girano anche senza qiskit.

## Come eseguire uno script

Dalla cartella radice del progetto:

```powershell
python quantum/01_algebra_calcolo/01_gate_come_matrici_unitarie.py
python quantum/02_ottica/01_polarizzazione_come_qubit.py
python quantum/03_meccanica_quantistica/01_stato_di_bell_entanglement.py
python quantum/04_elettronica_quantistica/01_oscillazioni_di_rabi.py
```

I grafici vengono salvati nella sottocartella `output/` della materia.

## Workflow "un commit al giorno"

1. Scegli la materia del giorno.
2. Crea un nuovo script numerato (es. `02_...`) partendo dal "Prossimo passo"
   suggerito in fondo allo script precedente.
3. Esegui e verifica l'output.
4. Aggiorna il `README.md` della materia con una riga sul lavoro svolto.
5. Commit con messaggio chiaro, ad esempio:

```bash
git add quantum/
git commit -m "ottica: beam splitter come gate di Hadamard"
git push
```

## Cosa NON viene pubblicato

Il materiale dei professori in `data/` e l'indice RAG in `agents/index/` sono
esclusi via `.gitignore` (contenuti potenzialmente protetti da copyright).
Su GitHub va solo **il mio codice**.
