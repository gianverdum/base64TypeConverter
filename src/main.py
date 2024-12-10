import logging
import traceback
from typing import Callable

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.routers import audio_converter

app = FastAPI(
    title="Base64 Type Converter API",
    description="API for converting audio files in Base64 to formats accepted by OpenAI.",
    version="1.0.0",
    contact={
        "name": "Giancarlo Verdum",
        "url": "https://github.com/gianverdum/base64TypeConverter",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


logging.basicConfig(level=logging.DEBUG)


@app.middleware("http")
async def error_handler(request: Request, call_next: Callable[[Request], JSONResponse]) -> JSONResponse:
    """
    Middleware for handling errors with detailed responses.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable[[Request], JSONResponse]): The next middleware or endpoint to call.

    Returns:
        JSONResponse: The HTTP response.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.error(f"Unexpected error: {e}\n{error_trace}")
        return JSONResponse(
            status_code=500,
            content={
                "detail": "An unexpected error occurred",
                "error": str(e),
                "traceback": error_trace,
            },
        )


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Root endpoint", response_description="Welcome message")
def read_root() -> dict[str, str]:
    """
    Root endpoint providing a welcome message.

    Returns:
        dict[str, str]: A JSON welcome message.
    """
    return {"message": "Welcome to the Base64 Type Converter API"}


app.include_router(audio_converter.router, tags=["Audio Converter"])
