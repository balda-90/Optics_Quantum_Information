from pathlib import Path
from typing import Dict, Optional, List

from dotenv import load_dotenv
import yaml

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


def load_config(config_path: Path) -> Dict:
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_vectorstore():
    """
    Restituisce un'istanza di Chroma caricata dal disco con lo stesso
    modello di embedding usato in ingestion.
    """
    load_dotenv()
    here = Path(__file__).parent
    cfg = load_config(here / "config.yaml")

    index_dir = (here / cfg["index_dir"]).resolve()
    embeddings = OpenAIEmbeddings(model=cfg["embeddings"]["model"])

    vs = Chroma(
        persist_directory=str(index_dir),
        embedding_function=embeddings,
    )
    return vs


def build_filters(corso: Optional[str] = None, tipo: Optional[str] = None) -> Dict:
    """
    Costruisce un dizionario di filtri per Chroma in base a corso/tipo.
    """
    where: Dict[str, str] = {}
    if corso:
        where["corso"] = corso
    if tipo:
        where["tipo"] = tipo
    return where


def search_context(
    query: str,
    corso: Optional[str] = None,
    tipo: Optional[str] = None,
    k: int = 6,
):
    """
    Esegue una ricerca semantica nell'indice vettoriale, con filtri opzionali.
    Ritorna una lista di Document.
    """
    vs = get_vectorstore()
    where = build_filters(corso=corso, tipo=tipo)
    if where:
        docs = vs.search(query, search_type="similarity", k=k, filter=where)
    else:
        docs = vs.search(query, search_type="similarity", k=k)
    return docs


def search_across_courses(
    query: str,
    corsi: Optional[List[str]] = None,
    tipo: Optional[str] = None,
    k: int = 8,
):
    """
    Cerca su una lista di corsi specifici (o su tutti se corsi è None).
    """
    vs = get_vectorstore()

    if corsi:
        all_docs = []
        for corso in corsi:
            where = build_filters(corso=corso, tipo=tipo)
            docs = vs.search(query, search_type="similarity", k=max(1, k // len(corsi)), filter=where)
            all_docs.extend(docs)
        return all_docs
    else:
        where = build_filters(tipo=tipo)
        return vs.search(query, search_type="similarity", k=k, filter=where or None)

