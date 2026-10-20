from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="A text description of the desired image(s).")
    model: Optional[str] = Field("perchance", description="Model or style name (e.g. perchance, perchance-cinematic, perchance-anime).")
    n: Optional[int] = Field(1, ge=1, le=4, description="The number of images to generate.")
    size: Optional[str] = Field("1024x1024", description="Image resolution (1024x1024 [1:1], 1792x1024 [16:9], 1024x1792 [9:16]).")
    response_format: Optional[Literal["url", "b64_json"]] = Field("b64_json", description="The format in which the generated images are returned.")
    style: Optional[str] = Field(None, description="Explicit art style to apply (e.g., Cinematic, Painted Anime, Casual Photo).")
    negative_prompt: Optional[str] = Field(None, description="Elements to avoid in the generation.")


class ImageData(BaseModel):
    b64_json: Optional[str] = None
    url: Optional[str] = None
    revised_prompt: Optional[str] = None


class ImageResponse(BaseModel):
    created: int
    data: List[ImageData]


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = 1700000000
    owned_by: str = "perchance"


class ModelListResponse(BaseModel):
    object: str = "list"
    data: List[ModelCard]
