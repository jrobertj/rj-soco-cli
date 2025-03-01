import os
from pathlib import Path

from gtts import gTTS

from soco_cli.utils import error_report

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame


def create_tts_file(text: str, tts_file_path: Path=Path("tts.mp3"), lang='no'):
    """
    Create a Text-to-Speech (TTS) file using the provided text.

    Args:
        text (str): The text to convert to speech.
        tts_file_path (Path, optional): The file path where the TTS file will be saved. Defaults to 'tts.mp3'.
        lang (str, optional): The language for the TTS. Defaults to 'no' (Norwegian).
    """

    if tts_file_path.exists():
        # Delete the file if it already exists:
        tts_file_path.unlink()

    tts = gTTS(text=text, lang=lang)
    tts.save(str(tts_file_path))


# TODO Consider using this function instead of the gTTS library:
def create_tts_file_cloud(text: str, tts_file_path: Path = Path("tts.mp3"), language_code="nb-NO", voice_name="nb-NO-Wavenet-B"):
    """
    Create a Text-to-Speech (TTS) file using Google Cloud Text-to-Speech.

    Args:
        text (str): The text to convert to speech.
        tts_file_path (Path, optional): The file path where the TTS file will be saved. Defaults to 'tts.mp3'.
        language_code (str, optional): The language code for the TTS. Defaults to 'nb-NO' (Norwegian Bokmål).
        voice_name (str, optional): The name of the voice to use. Defaults to 'nb-NO-Wavenet-B' (a female Norwegian voice).

    Note 1:
        You need to install the Google Cloud Text-to-Speech library:
            pip install google-cloud-texttospeech

    Note 2:
        You need to set up a Google Cloud project and enable the Text-to-Speech API.

        Create a service account and download the service account key file (JSON).
        Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your key file.
        See the google cloud documentation for details on how to do this.

    Note 3:
        Finding Voice Names:
            Refer to the Google Cloud Text-to-Speech documentation to find a list of available voice names for your desired language.
            You can also list the available voices programmatically using the client.list_voices method.
    """

    from google.cloud import texttospeech

    if tts_file_path.exists():
        tts_file_path.unlink()

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(str(tts_file_path), "wb") as out:
        out.write(response.audio_content)


def play_mp3_file(file_path: Path):
    """Plays a mp3 file on the local host using pygame."""
    if file_path.exists():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10) #keep program running while music plays.
            pygame.mixer.quit()

        except pygame.error as e:
            error_report(f"Error playing MP3: {e}")
        except Exception as e:
            error_report(f"General Error playing MP3: {e}")
    else:
        error_report(f"File not found: {file_path}")
