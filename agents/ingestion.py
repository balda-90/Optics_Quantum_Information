import os
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
from tqdm import tqdm
import yaml

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from .ocr_utils import image_to_text


def load_config(config_path: Path) -> Dict:
    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_course_and_type(file_path: Path, data_root: Path) -> Dict[str, str]:
    """
    Estrae metadati (corso, tipo) dalla struttura:
    data/corso_nome/{slide,appunti,esercizi}/file.pdf
    """
    try:
        rel = file_path.relative_to(data_root)
    except ValueError:
        return {"corso": "sconosciuto", "tipo": "sconosciuto"}

    parts = rel.parts
    corso = parts[0] if len(parts) > 0 else "sconosciuto"
    tipo = parts[1] if len(parts) > 1 else "sconosciuto"
    return {"corso": corso, "tipo": tipo}


def iter_files(data_root: Path) -> List[Path]:
    # Includiamo anche immagini (foto/scansioni di appunti)
    exts = {".pdf", ".txt", ".md", ".png", ".jpg", ".jpeg"}
    files: List[Path] = []
    for root, _, filenames in os.walk(data_root):
        for name in filenames:
            p = Path(root) / name
            if p.suffix.lower() in exts:
                files.append(p)
    return files


def load_documents_for_file(file_path: Path):
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
        return loader.load()
    if suffix in {".png", ".jpg", ".jpeg"}:
        # OCR su immagini di appunti
        text = image_to_text(file_path)
        doc = Document(page_content=text, metadata={"source_path": str(file_path), "filename": file_path.name})
        return [doc]

    # txt / md
    loader = TextLoader(str(file_path), encoding="utf-8")
    return loader.load()


def build_index(config_path: str | Path) -> None:
    """
    Costruisce o ricostruisce l'indice vettoriale Chroma a partire dai file in data/.
    """
    load_dotenv()

    cfg = load_config(Path(config_path))
    data_root = (Path(__file__).parent / cfg["data_dir"]).resolve()
    index_dir = (Path(__file__).parent / cfg["index_dir"]).resolve()

    data_root.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)

    files = iter_files(data_root)
    if not files:
        print(f"Nessun file trovato in {data_root}. Aggiungi materiale in data/ e riprova.")
        return

    print(f"Trovati {len(files)} file da indicizzare sotto {data_root}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg["ingestion"]["chunk_size"],
        chunk_overlap=cfg["ingestion"]["chunk_overlap"],
    )

    all_chunks = []
    for fpath in tqdm(files, desc="Caricamento documenti"):
        docs = load_documents_for_file(fpath)
        meta_base = get_course_and_type(fpath, data_root)
        for d in docs:
            d.metadata.update(
                {
                    "source_path": str(fpath),
                    "filename": fpath.name,
                    "corso": meta_base["corso"],
                    "tipo": meta_base["tipo"],
                }
            )
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("Nessun chunk creato dall'ingestion.")
        return

    embeddings = OpenAIEmbeddings(model=cfg["embeddings"]["model"])

    print(f"Costruzione indice Chroma in {index_dir} ...")
    Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        persist_directory=str(index_dir),
    )
    print("Indicizzazione completata.")


if __name__ == "__main__":
    here = Path(__file__).parent
    build_index(here / "config.yaml")

