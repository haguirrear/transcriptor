import io
from fastapi import UploadFile
from pydub import AudioSegment
from backend.app.services.openai import openai_client

from backend.app.errors import ControlledException


async def generate_transcription(audio_file: UploadFile):
    if audio_file.content_type != "audio/mpeg":
        raise ControlledException("El archivo debe ser un MP3.")

    file_bytes = await audio_file.read()
    original_audio = AudioSegment.from_file(io.BytesIO(file_bytes), format="mp3")

    # Define el tamaño máximo de archivo en bytes (25 MB)
    max_size_bytes = 25 * 1024 * 1024
    # Calcula la duración total del audio en milisegundos
    total_duration = len(original_audio)

    # Inicializa una lista para guardar las transcripciones de cada segmento
    transcriptions = []

    # Si el archivo es más grande de lo permitido, divídelo y procesa cada segmento
    if len(file_bytes) > max_size_bytes:
        # Divide el audio en segmentos de menos de 25 MB
        for start_ms in range(
            0, total_duration, 10 * 60 * 1000
        ):  # Segmentos de hasta 10 minutos
            # Calcula el final del segmento actual
            end_ms = start_ms + 10 * 60 * 1000
            # Asegúrate de no sobrepasar la duración total del audio
            segment = (
                original_audio[start_ms:end_ms]
                if end_ms < total_duration
                else original_audio[start_ms:]
            )

            # Convierte el segmento a bytes
            segment_buffer = io.BytesIO()
            segment.export(segment_buffer, format="mp3")
            segment_bytes = segment_buffer.getvalue()

            # Crea un objeto BytesIO para el segmento
            file_segment = io.BytesIO(segment_bytes)
            file_segment.name = f"segment_{start_ms}.mp3"

            # Realiza la transcripción del segmento
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=file_segment,
                response_format="text",
            )

            # Agrega la transcripción del segmento a la lista de transcripciones
            transcriptions.append(transcription)
    else:
        # Si el archivo es menor de 25 MB, procésalo directamente
        file = io.BytesIO(file_bytes)
        file.name = audio_file.filename

        transcription = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            response_format="text",
        )
        transcriptions.append(transcription)

    # Combina todas las transcripciones en una sola cadena
    final_transcription = " ".join(transcriptions)
    return final_transcription
