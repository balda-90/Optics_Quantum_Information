from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
import yaml

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from . import retrieval


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


def _format_docs(docs) -> str:
    lines: List[str] = []
    for i, d in enumerate(docs, start=1):
        meta = d.metadata or {}
        header = f"[{i}] corso={meta.get('corso','?')} tipo={meta.get('tipo','?')} file={meta.get('filename','?')}"
        lines.append(header)
        lines.append(d.page_content.strip())
        lines.append("")
    return "\n".join(lines)


def answer_question(
    query: str,
    corso: Optional[str] = None,
    tipo: Optional[str] = None,
    k: int = 6,
) -> str:
    """
    Q&A generale sui materiali, filtrabile per corso/tipo.
    """
    docs = retrieval.search_context(query, corso=corso, tipo=tipo, k=k)
    context = _format_docs(docs)
    llm = get_llm()

    system = SystemMessage(
        content=(
            "Sei un assistente per lo studio di un master in Ottica e Quantum Information. "
            "Usa SOLO le informazioni nel CONTENUTO per rispondere. "
            "Cita esplicitamente a quali corsi/materiali ti stai riferendo. "
            "Rispondi in italiano chiaro e conciso."
        )
    )
    human = HumanMessage(
        content=f"CONTENUTO:\n{context}\n\nDOMANDA:\n{query}"
    )
    resp = llm.invoke([system, human])
    return resp.content


def compare_notes_and_slides(
    query: str,
    corso: str,
    k: int = 4,
) -> str:
    """
    Confronta appunti e slide per un corso su un certo argomento.
    """
    docs_slide = retrieval.search_context(query, corso=corso, tipo="slide", k=k)
    docs_appunti = retrieval.search_context(query, corso=corso, tipo="appunti", k=k)

    context_slide = _format_docs(docs_slide)
    context_app = _format_docs(docs_appunti)

    llm = get_llm()
    system = SystemMessage(
        content=(
            "Ti vengono forniti estratti di SLIDE e APPUNTI dello stesso corso.\n"
            "- Prima riassumi brevemente i punti chiave comuni.\n"
            "- Poi elenca cosa compare SOLO nelle slide.\n"
            "- Poi cosa compare SOLO negli appunti.\n"
            "Se qualche parte manca completamente dillo esplicitamente."
        )
    )
    human = HumanMessage(
        content=(
            f"SLIDE (corso={corso}):\n{context_slide}\n\n"
            f"APPUNTI (corso={corso}):\n{context_app}\n\n"
            f"Argomento o domanda dello studente: {query}"
        )
    )
    resp = llm.invoke([system, human])
    return resp.content


def cross_course_links(
    query: str,
    corsi: Optional[List[str]] = None,
    tipo: Optional[str] = None,
    k: int = 8,
) -> str:
    """
    Cerca collegamenti tra corsi diversi su un certo concetto.
    """
    docs = retrieval.search_across_courses(query, corsi=corsi, tipo=tipo, k=k)
    context = _format_docs(docs)
    llm = get_llm()

    system = SystemMessage(
        content=(
            "Ti vengono forniti estratti da più corsi del master.\n"
            "Il tuo compito è:\n"
            "- individuare collegamenti concettuali tra i corsi;\n"
            "- evidenziare prerequisiti e differenze di punto di vista;\n"
            "- proporre una breve mappa concettuale testuale per lo studente."
        )
    )
    human = HumanMessage(
        content=(
            f"ESTRATTI DA PIÙ CORSI:\n{context}\n\n"
            f"Richiesta/argomento dello studente: {query}"
        )
    )
    resp = llm.invoke([system, human])
    return resp.content


def exam_prep_for_course(
    corso: str,
    k: int = 10,
) -> str:
    """
    Genera un aiuto per la preparazione d'esame a partire da slide/appunti di un corso.
    """
    query = "struttura generale del corso, argomenti principali, risultati chiave"
    docs = retrieval.search_context(query, corso=corso, tipo=None, k=k)
    context = _format_docs(docs)

    llm = get_llm()
    system = SystemMessage(
        content=(
            "Sei un assistente che aiuta a preparare un esame universitario.\n"
            "Dai contenuti forniti devi:\n"
            "- ricavare un elenco di macro-argomenti del corso;\n"
            "- per ciascuno, proporre 2-4 possibili domande d'esame (orali o scritte);\n"
            "- suggerire un breve piano di studio in passi ordinati."
        )
    )
    human = HumanMessage(
        content=(
            f"CONTENUTI DEL CORSO {corso}:\n{context}\n\n"
            "Genera schema di preparazione esame come indicato."
        )
    )
    resp = llm.invoke([system, human])
    return resp.content

