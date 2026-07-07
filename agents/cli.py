import os
from pathlib import Path

from dotenv import load_dotenv

from . import agent


def ensure_api_key():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("ATTENZIONE: non è impostata la variabile d'ambiente OPENAI_API_KEY.")
        print("Impostala nel tuo sistema o in un file .env nella cartella del progetto.")


def ask_course(prompt: str) -> str:
    corso = input(prompt).strip()
    return corso or ""


def main():
    here = Path(__file__).parent
    print("Assistente master OQI - CLI")
    print(f"Cartella agenti: {here}")
    print("-" * 50)

    ensure_api_key()

    while True:
        print("\nScegli un'operazione:")
        print("1) Q&A generale sui materiali")
        print("2) Confronta appunti e slide per un corso")
        print("3) Trova collegamenti tra corsi")
        print("4) Preparazione esame per un corso")
        print("0) Esci")
        choice = input("Scelta: ").strip()

        if choice == "0":
            print("Uscita.")
            break
        elif choice == "1":
            query = input("Domanda (es. spiegami X): ").strip()
            corso = input("Filtra per corso (invio per tutti): ").strip() or None
            tipo = input("Filtra per tipo (slide/appunti/esercizi, invio per tutti): ").strip() or None
            print("\nSto recuperando il contesto e generando la risposta...\n")
            try:
                answer = agent.answer_question(query, corso=corso, tipo=tipo)
                print(answer)
            except Exception as e:
                print(f"Errore durante la generazione della risposta: {e}")
        elif choice == "2":
            corso = ask_course("Nome del corso: ")
            query = input("Argomento o domanda (es. 'trasformata di Fourier'): ").strip()
            print("\nConfronto appunti/slide in corso...\n")
            try:
                answer = agent.compare_notes_and_slides(query=query, corso=corso)
                print(answer)
            except Exception as e:
                print(f"Errore durante il confronto: {e}")
        elif choice == "3":
            query = input("Concetto o domanda su cui cercare collegamenti: ").strip()
            raw = input("Elenco corsi separati da virgola (invio per usarli tutti): ").strip()
            corsi = [c.strip() for c in raw.split(",") if c.strip()] or None
            print("\nRicerca collegamenti tra corsi...\n")
            try:
                answer = agent.cross_course_links(query=query, corsi=corsi)
                print(answer)
            except Exception as e:
                print(f"Errore durante la ricerca collegamenti: {e}")
        elif choice == "4":
            corso = ask_course("Nome del corso: ")
            print("\nGenerazione schema di preparazione esame...\n")
            try:
                answer = agent.exam_prep_for_course(corso=corso)
                print(answer)
            except Exception as e:
                print(f"Errore durante la preparazione esame: {e}")
        else:
            print("Scelta non valida, riprova.")


if __name__ == "__main__":
    main()

