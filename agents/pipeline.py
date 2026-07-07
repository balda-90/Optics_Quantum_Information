from pathlib import Path

from . import ingestion
from . import knowledge_graph


def run_full_pipeline():
    """
    Esegue l'intera pipeline:
    1) ingestion dei dati in data/ e costruzione dell'indice vettoriale;
    2) costruzione del knowledge graph per tutti i corsi trovati;
    3) esportazione dei file markdown navigabili per ciascun corso.
    """
    here = Path(__file__).parent
    config_path = here / "config.yaml"

    print("=== STEP 1: Ingestion e costruzione indice vettoriale ===")
    ingestion.build_index(config_path)

    print("\n=== STEP 2: Costruzione knowledge graph per tutti i corsi ===")
    knowledge_graph.build_knowledge_graph_for_all_courses()


if __name__ == "__main__":
    run_full_pipeline()

