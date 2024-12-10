# src/services/audio_service.py
import base64
import io

from pydub import AudioSegment
from pydub.utils import which

from src.schemas.audio import AudioBase64Request, AudioBase64Response

# Configuring the path to ffmpeg and ffprobe
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

SUPPORTED_FORMATS = ["mp3", "wav", "ogg", "m4a", "flac", "webm"]


def process_audio(audio_request: AudioBase64Request) -> AudioBase64Response:
    """
    Processes the given audio file in base64 format.
    Converts unsupported formats to MP3 and returns the converted file.

    Parameters:
        audio_request (AudioBase64Request): The input audio file in base64 format.

    Returns:
        dict: Information about the processed audio file.
    """
    try:
        # Decode the base64 string
        audio_data = base64.b64decode(audio_request.base64_audio)
        audio_stream = io.BytesIO(audio_data)

        # Detect the file format
        audio = AudioSegment.from_file(audio_stream)
        original_format = audio.format

        if original_format in SUPPORTED_FORMATS:
            return AudioBase64Response(
                original_format=original_format,
                converted_format=original_format,
                base64_audio=audio_request.base64_audio,
            )

        # Convert to MP3 if the format is unsupported
        output_stream = io.BytesIO()
        audio.export(output_stream, format="mp3")
        output_stream.seek(0)

        converted_base64 = base64.b64encode(output_stream.read()).decode("utf-8")
        return AudioBase64Response(
            original_format=original_format,
            converted_format="mp3",
            base64_audio=converted_base64,
        )

    except Exception as e:
        raise ValueError(f"Error processing audio: {str(e)}")
