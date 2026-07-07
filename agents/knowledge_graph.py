import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set

from dotenv import load_dotenv
import yaml

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from .retrieval import get_vectorstore


def load_config() -> Dict:
    here = Path(__file__).parent
    with (here / "config.yaml").open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_llm():
    load_dotenv()
    cfg = load_config()
    model = cfg["llm"]["model"]
    temperature = cfg["llm"].get("temperature", 0.2)
    return ChatOpenAI(model=model, temperature=temperature)


def _get_all_docs_for_course(corso: str, k: int = 80):
    """
    Recupera un campione ampio di documenti per un corso, mescolando tipi diversi.
    """
    vs = get_vectorstore()
    # Query generica per coprire il più possibile il corso
    query = "argomenti principali e risultati chiave del corso"
    where = {"corso": corso}
    docs = vs.search(query, search_type="similarity", k=k, filter=where)
    return docs


def _build_kg_from_docs(corso: str, docs) -> Dict:
    """
    Usa l'LLM per estrarre un grafo concettuale in formato JSON da una collezione di Document.
    """
    llm = get_llm()

    # Costruisci un contesto relativamente compatto
    snippets: List[str] = []
    for d in docs:
        txt = d.page_content.strip().replace("\n", " ")
        if len(txt) > 500:
            txt = txt[:500] + " ..."
        snippets.append(txt)
    context = "\n".join(f"- {s}" for s in snippets)

    system_msg = SystemMessage(
        content=(
            "Sei un assistente che estrae knowledge graph da materiale universitario.\n"
            "Dato un insieme di estratti di un corso, devi produrre un JSON con nodi e archi.\n"
            "Schema richiesto (JSON):\n"
            "{\n"
            '  \"nodes\": [ {\"id\": \"string\", \"label\": \"string\"}, ...],\n'
            '  \"edges\": [ {\"source\": \"id_nodo\", \"target\": \"id_nodo\", \"relation\": \"string\"}, ...]\n'
            "}\n"
            "I nodi devono essere concetti (es. 'Qubit', 'Trasformata di Fourier', 'Operatore di Pauli').\n"
            "Gli archi devono esprimere relazioni semplici (es. 'usa', 'è_prerequisito_di', 'è_parte_di').\n"
            "Rispondi SOLO con il JSON, senza testo aggiuntivo."
        )
    )

    user_msg = HumanMessage(
        content=(
            f"Estratti del corso '{corso}':\n{context}\n\n"
            "Ora genera il JSON del knowledge graph come da schema."
        )
    )

    resp = llm.invoke([system_msg, user_msg])
    content = resp.content
    try:
        kg = json.loads(content)
    except json.JSONDecodeError:
        # In caso di risposta non perfettamente JSON, prova a trovare una sottostringa JSON.
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            kg = json.loads(content[start : end + 1])
        else:
            raise
    return kg


def save_kg(corso: str, kg: Dict) -> Path:
    here = Path(__file__).parent
    kg_dir = here / "index" / "kg"
    kg_dir.mkdir(parents=True, exist_ok=True)
    path = kg_dir / f"{corso}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(kg, f, ensure_ascii=False, indent=2)
    return path


def _collect_courses_from_index() -> Set[str]:
    """
    Legge tutte le metadate dall'indice e ricava l'elenco dei corsi presenti.
    """
    vs = get_vectorstore()
    # Chroma wrapper espone get per recuperare tutti i metadati
    raw = vs.get(include=["metadatas"])
    courses: Set[str] = set()
    for meta in raw.get("metadatas", []):
        if not meta:
            continue
        corso = meta.get("corso")
        if corso:
            courses.add(corso)
    return courses


def export_markdown_for_course(corso: str, kg: Dict) -> Path:
    """
    Esporta il knowledge graph di un corso in un file markdown navigabile.
    """
    nodes = kg.get("nodes", [])
    edges = kg.get("edges", [])

    # Map da id nodo a label
    id_to_label = {n["id"]: n.get("label", n["id"]) for n in nodes if "id" in n}

    outgoing: Dict[str, List[Dict]] = defaultdict(list)
    incoming: Dict[str, List[Dict]] = defaultdict(list)

    for e in edges:
        src = e.get("source")
        tgt = e.get("target")
        rel = e.get("relation", "")
        if src and tgt:
            outgoing[src].append({"target": tgt, "relation": rel})
            incoming[tgt].append({"source": src, "relation": rel})

    lines: List[str] = []
    lines.append(f"# Knowledge Graph - {corso}")
    lines.append("")
    lines.append("## Concetti principali")
    lines.append("")

    for node_id, label in id_to_label.items():
        lines.append(f"### {label}")
        lines.append(f"- ID: `{node_id}`")
        if outgoing.get(node_id):
            lines.append("- Relazioni in uscita:")
            for rel in outgoing[node_id]:
                tgt_label = id_to_label.get(rel["target"], rel["target"])
                lines.append(f"  - ({rel['relation']}) → **{tgt_label}**")
        if incoming.get(node_id):
            lines.append("- Relazioni in entrata:")
            for rel in incoming[node_id]:
                src_label = id_to_label.get(rel["source"], rel["source"])
                lines.append(f"  - **{src_label}** → ({rel['relation']})")
        lines.append("")

    here = Path(__file__).parent
    out_dir = here.parent / "organized"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{corso}.md"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return out_path


def build_knowledge_graph_for_all_courses() -> None:
    """
    Estrae l'elenco dei corsi dall'indice, costruisce e salva un knowledge graph
    per ciascuno, ed esporta i markdown corrispondenti.
    """
    courses = _collect_courses_from_index()
    if not courses:
        print("Nessun corso trovato nell'indice. Hai già eseguito l'ingestion?")
        return

    print(f"Trovati i seguenti corsi nell'indice: {', '.join(sorted(courses))}")

    for corso in sorted(courses):
        print(f"\nCostruzione knowledge graph per il corso: {corso}")
        docs = _get_all_docs_for_course(corso)
        if not docs:
            print(f"- Nessun documento trovato per il corso {corso}, salto.")
            continue
        kg = _build_kg_from_docs(corso, docs)
        kg_path = save_kg(corso, kg)
        md_path = export_markdown_for_course(corso, kg)
        print(f"- Salvato KG JSON in: {kg_path}")
        print(f"- Salvato markdown navigabile in: {md_path}")


if __name__ == "__main__":
    build_knowledge_graph_for_all_courses()

