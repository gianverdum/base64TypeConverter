from pydantic import BaseModel


class AudioBase64Request(BaseModel):
    base64_audio: str


class AudioBase64Response(BaseModel):
    original_format: str
    converted_format: str
    base64_audio: str
