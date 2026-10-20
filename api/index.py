import sys
import time
from pathlib import Path
from typing import Optional

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import API_KEY, AVAILABLE_MODELS
from core.perchance_client import PerchanceClient
from core.openai_types import (
    ImageGenerationRequest,
    ImageResponse,
    ImageData,
    ModelCard,
    ModelListResponse,
)

app = FastAPI(
    title="Perchance OpenAI V1 Image API",
    description="OpenAI V1 Compatible Image Generation API powered by Perchance AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def vercel_path_normalizer(request: Request, call_next):
    path = request.scope.get("path", "")
    if path.startswith("/api/index.py"):
        normalized = path[len("/api/index.py"):]
        request.scope["path"] = normalized if normalized else "/"
    return await call_next(request)


security = HTTPBearer(auto_error=False)


def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)):
    """Validates API key if configured in environment."""
    if not API_KEY:
        return True
    if not credentials or credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={"error": {"message": "Invalid API key provided.", "type": "invalid_request_error"}}
        )
    return True


# Global client instance
generator_client = PerchanceClient(headless=True)


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Perchance AI Text-to-Image API (OpenAI Compatible)",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/v1/images/generations", "/v1/models", "/health"],
    }


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": int(time.time())}


@app.get("/v1/models", response_model=ModelListResponse)
async def list_models(_: bool = Depends(verify_api_key)):
    models = [ModelCard(id=m["id"]) for m in AVAILABLE_MODELS]
    return ModelListResponse(data=models)


@app.post("/v1/images/generations", response_model=ImageResponse)
async def generate_image(request: ImageGenerationRequest, _: bool = Depends(verify_api_key)):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail={"error": {"message": "Prompt is required.", "type": "invalid_request_error"}}
        )

    try:
        b64_images = generator_client.generate(
            prompt=request.prompt,
            model=request.model,
            style=request.style,
            size=request.size,
            negative_prompt=request.negative_prompt,
            num_images=request.n or 1,
            disable_safety_settings=True,
        )

        data = []
        for b64 in b64_images:
            if request.response_format == "url":
                # For serverless, return data URI URL
                data.append(ImageData(url=f"data:image/png;base64,{b64}", revised_prompt=request.prompt))
            else:
                data.append(ImageData(b64_json=b64, revised_prompt=request.prompt))

        return ImageResponse(
            created=int(time.time()),
            data=data
        )

    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail={"error": {"message": str(err), "type": "api_error"}}
        )
