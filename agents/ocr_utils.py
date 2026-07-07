from pathlib import Path
from typing import Optional
import os

import pytesseract
from PIL import Image


def configure_tesseract(tesseract_cmd: Optional[str] = None) -> None:
    """
    Configura il path di Tesseract se necessario.
    - Se tesseract_cmd è passato, usa quello.
    - Altrimenti, se esiste la variabile d'ambiente TESSERACT_CMD, usa quella.

    Su Windows, se Tesseract è nel PATH di sistema, di solito non serve fare nulla.
    """
    cmd: Optional[str] = None

    if tesseract_cmd:
        cmd = tesseract_cmd
    else:
        # Prova a leggere dalla variabile d'ambiente dedicata
        cmd = os.getenv("TESSERACT_CMD")

        # Se non è impostata, su Windows prova il percorso di default
        if not cmd and os.name == "nt":
            default_path = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
            if default_path.exists():
                cmd = str(default_path)

    if cmd:
        pytesseract.pytesseract.tesseract_cmd = cmd


def image_to_text(path: Path, lang: str = "ita+eng") -> str:
    """
    Converte un'immagine (foto/scansione di appunti) in testo usando Tesseract OCR.
    - lang: codici lingua Tesseract, es. 'ita', 'eng', 'ita+eng'.
    """
    # Garantisce che Tesseract sia configurato (PATH, variabile o percorso di default Windows)
    configure_tesseract()

    image = Image.open(path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text

