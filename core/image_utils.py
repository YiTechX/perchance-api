import base64
import io
from PIL import Image

def clean_b64(raw_data: str) -> str:
    """Strips data URI prefix if present and returns clean base64 string."""
    if raw_data.startswith("data:"):
        return raw_data.split(",", 1)[1]
    return raw_data

def b64_to_bytes(b64_str: str) -> bytes:
    """Decodes base64 string into binary bytes."""
    return base64.b64decode(clean_b64(b64_str))

def bytes_to_b64(data: bytes, mime_type: str = "image/png") -> str:
    """Encodes binary bytes to base64 string."""
    return base64.b64encode(data).decode("utf-8")
