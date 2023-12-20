import io
from fastapi import UploadFile
from transcriptor.services.openai import openai_client

from transcriptor.errors import ControlledException


async def generate_transcription(audio_file: UploadFile):
    if audio_file.content_type != "audio/mpeg":
        raise ControlledException("El archivo debe ser un MP3.")

        # Validar el tamaño del archivo (25 MB = 25 * 1024 * 1024 bytes)
    if audio_file.size and audio_file.size > 25 * 1024 * 1024:
        raise ControlledException("El archivo no debe superar los 25 MB.")

    file_bytes = await audio_file.read()

    file = io.BytesIO(file_bytes)
    file.name = audio_file.filename

    transcription = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=file,
        response_format="text",
    )

    return transcription
