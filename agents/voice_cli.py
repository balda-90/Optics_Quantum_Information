import os
import tempfile
from pathlib import Path

import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from openai import OpenAI

from . import agent


def ensure_api_key():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("ATTENZIONE: non è impostata la variabile d'ambiente OPENAI_API_KEY.")
        print("Impostala nel tuo sistema o in un file .env nella cartella del progetto.")
        return False
    return True


def record_audio(duration: float = 20.0, samplerate: int = 16000) -> Path:
    """
    Registra audio dal microfono per 'duration' secondi e lo salva in un file WAV temporaneo.
    """
    print(f"Registrazione per {duration} secondi... parla pure.")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="float32")
    sd.wait()

    tmp_dir = Path(tempfile.gettempdir())
    wav_path = tmp_dir / "oqi_question.wav"
    sf.write(wav_path, audio, samplerate)
    print(f"Registrazione salvata in {wav_path}")
    return wav_path


def transcribe_audio(file_path: Path) -> str:
    """
    Usa OpenAI Whisper per trascrivere l'audio in testo.
    """
    client = OpenAI()
    with file_path.open("rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text",
        )
    return transcript


def speak_text(text: str) -> None:
    """
    Usa OpenAI text-to-speech per generare un file audio e lo apre con il player di default di Windows.
    """
    client = OpenAI()
    speech_file_path = Path(tempfile.gettempdir()) / "oqi_answer.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    ) as response:
        response.stream_to_file(speech_file_path)

    print(f"Risposta audio salvata in {speech_file_path}")
    try:
        os.startfile(speech_file_path)  # type: ignore[attr-defined]
    except Exception:
        print("Impossibile aprire automaticamente il player audio. Riproduci il file manualmente.")


def main():
    here = Path(__file__).parent
    print("Assistente master OQI - VOICE CLI")
    print(f"Cartella agenti: {here}")
    print("-" * 50)

    if not ensure_api_key():
        return

    print("Questo modo usa la voce per fare domande.")
    print("Flusso tipico:")
    print("- Premi INVIO per iniziare una registrazione (durata fissa).")
    print("- Parla, attendi la fine.")
    print("- La domanda viene trascritta e inviata all'agente Q&A.")
    print("- La risposta è mostrata a schermo e letta a voce.")

    while True:
        cmd = input("\nPremi INVIO per fare una domanda vocale, oppure 'q' per uscire: ").strip().lower()
        if cmd == "q":
            print("Uscita.")
            break

        wav_path = record_audio()
        print("Trascrizione in corso...")
        try:
            text_question = transcribe_audio(wav_path)
        except Exception as e:
            print(f"Errore nella trascrizione: {e}")
            continue

        print(f"\nTesto riconosciuto:\n{text_question}\n")
        print("Sto recuperando il contesto e generando la risposta...\n")
        try:
            answer = agent.answer_question(text_question)
        except Exception as e:
            print(f"Errore nella generazione della risposta: {e}")
            continue

        print("Risposta testuale:\n")
        print(answer)

        try:
            print("\nGenerazione risposta audio...")
            speak_text(answer)
        except Exception as e:
            print(f"Errore nella sintesi vocale: {e}")


if __name__ == "__main__":
    main()

