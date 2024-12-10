# src/router/audio_converter.py
from fastapi import APIRouter, status

from src.schemas.audio import AudioBase64Request, AudioBase64Response
from src.services.audio_service import process_audio

router = APIRouter()


@router.post(
    "/api/audio/convert/",
    response_model=AudioBase64Response,
    status_code=status.HTTP_200_OK,
    summary="Convert or validate audio file format",
    responses={
        200: {
            "description": "Audio file processed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "original_format": "opus",
                        "converted_format": "mp3",
                        "base64_audio": "BASE64_STRING_HERE",
                    }
                }
            },
        },
        400: {"description": "Invalid audio format or processing error"},
    },
)
async def convert_audio_route(audio_request: AudioBase64Request) -> AudioBase64Response:
    """
    Endpoint to process audio files in base64 format.

    Parameters:
        audio_request (AudioBase64Request): The audio file in base64 format.

    Returns:
        AudioBase64Response: Processed audio details with base64 string.
    """
    return process_audio(audio_request)
