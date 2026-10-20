import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY", "").strip()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "perchance").strip()

# Model names mapped to art style presets
MODEL_STYLE_MAPPINGS = {
    "perchance": None,
    "perchance-default": None,
    "dall-e-3": None,
    "dall-e-2": None,
    "perchance-cinematic": "Cinematic",
    "perchance-anime": "Painted Anime",
    "perchance-ghibli": "Studio Ghibli",
    "perchance-photo": "Casual Photo",
    "perchance-disney": "3D Disney Character",
    "perchance-oil": "Oil Painting",
    "perchance-pixel": "Pixel Art",
    "perchance-digital": "Digital Painting",
    "perchance-cyberpunk": "Cyberpunk",
    "perchance-concept": "Concept Art",
}

AVAILABLE_MODELS = [
    {"id": "perchance", "name": "Perchance AI Default"},
    {"id": "perchance-cinematic", "name": "Perchance Cinematic Style"},
    {"id": "perchance-anime", "name": "Perchance Anime Style"},
    {"id": "perchance-ghibli", "name": "Perchance Studio Ghibli Style"},
    {"id": "perchance-photo", "name": "Perchance Casual Photo Style"},
    {"id": "perchance-disney", "name": "Perchance 3D Disney Style"},
    {"id": "perchance-digital", "name": "Perchance Digital Painting Style"},
    {"id": "perchance-cyberpunk", "name": "Perchance Cyberpunk Style"},
    {"id": "perchance-pixel", "name": "Perchance Pixel Art Style"},
]

# Standard OpenAI image sizes mapped to Perchance resolutions
SIZE_TO_SHAPE = {
    # 1:1 Square
    "1024x1024": "768x768",
    "512x512": "768x768",
    "1:1": "768x768",
    "square": "768x768",
    # 16:9 Landscape
    "1792x1024": "768x512",
    "1920x1080": "768x512",
    "1280x720": "768x512",
    "16:9": "768x512",
    "landscape": "768x512",
    # 9:16 Portrait
    "1024x1792": "512x768",
    "1080x1920": "512x768",
    "720x1280": "512x768",
    "9:16": "512x768",
    "portrait": "512x768",
}

def resolve_shape(size_str: str | None) -> str:
    if not size_str:
        return "768x768"
    clean = size_str.strip().lower()
    return SIZE_TO_SHAPE.get(clean, "768x768")

def resolve_style_from_model(model_id: str | None) -> str | None:
    if not model_id:
        return None
    clean = model_id.strip().lower()
    return MODEL_STYLE_MAPPINGS.get(clean, None)
