import time
from typing import Optional, Dict, Any, List
import perchancy
from core.config import resolve_shape, resolve_style_from_model
from core.image_utils import clean_b64


class PerchanceClient:
    """Singleton-style or on-demand Perchance generator client."""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self._client: Optional[perchancy.Client] = None

    def _get_client(self) -> perchancy.Client:
        if self._client is None:
            self._client = perchancy.Client(headless=self.headless)
        return self._client

    def close(self) -> None:
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        style: Optional[str] = None,
        size: Optional[str] = "1024x1024",
        negative_prompt: Optional[str] = None,
        num_images: int = 1,
        disable_safety_settings: bool = True,
        timeout: int = 90,
    ) -> List[str]:
        """
        Generates images and returns a list of base64 data strings.
        """
        client = self._get_client()

        resolution = resolve_shape(size)
        effective_style = style or resolve_style_from_model(model)

        extra_params: Dict[str, Any] = {
            "shape": resolution,
        }
        if effective_style:
            extra_params["style"] = effective_style

        final_prompt = prompt.strip()
        if negative_prompt and negative_prompt.strip():
            final_prompt = f"{final_prompt} [negative: {negative_prompt.strip()}]"

        res = client.images.generate(
            model="ai-text-to-image-generator",
            prompt=final_prompt,
            num_images=num_images,
            image_format="png",
            time_for_image=timeout,
            extra_params=extra_params,
            disable_safety_settings=disable_safety_settings,
        )

        if res.get("error"):
            raise RuntimeError(f"Generation failed: {res['error']}")

        data_items = res.get("data", [])
        if not data_items:
            raise RuntimeError("No image returned from engine.")

        results = []
        for item in data_items:
            raw_url = item.get("url", "")
            if raw_url:
                results.append(clean_b64(raw_url))

        return results
