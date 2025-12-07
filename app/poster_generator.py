import base64
from typing import Literal

from openai import OpenAI
from huggingface_hub import InferenceClient

from .config import settings
from .schemas import PosterRequest, PosterResponse


def build_poster_prompt(request: PosterRequest) -> str:
    base = (
        "Movie poster, cinematic composition, dramatic lighting, high detail, 4k. "
        'Design a poster for a movie with the following description: "{summary}". '
        "Include a central character and bold typography."
    )
    if request.style_hint:
        base += f" The style should feel {request.style_hint}."
    return base.format(summary=request.summary)


# ---------- OpenAI ----------


def _generate_with_openai(prompt: str) -> PosterResponse:
    if not settings.openai_api_key:
        raise RuntimeError("HF_API_KEY not set yet,IMAGE_PROVIDER=huggingface")

    client = OpenAI(api_key=settings.openai_api_key)

    result = client.images.generate(
        model=settings.image_model,
        prompt=prompt,
        size=settings.image_size,
        n=1,
    )
    url = result.data[0].url

    return PosterResponse(image_url=url, prompt=prompt)


# ---------- Hugging Face (HF Inference API, SDXL) ----------


def _generate_with_hf(prompt: str) -> PosterResponse:
    if not settings.hf_api_key:
        raise RuntimeError("HF_API_KEY not set yet,IMAGE_PROVIDER=huggingface")

    # Use the official Hugging Face InferenceClient
    client = InferenceClient(
        provider="hf-inference",
        api_key=settings.hf_api_key,
    )

    # This returns a PIL.Image.Image
    image = client.text_to_image(
        prompt,
        model=settings.hf_model,
    )

    # Encode image to base64 data URL (PNG)
    import io

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{b64}"

    return PosterResponse(image_url=data_url, prompt=prompt)


# ---------- Public entry ----------


def generate_poster(request: PosterRequest) -> PosterResponse:
    prompt = build_poster_prompt(request)

    provider: Literal["openai", "huggingface"] = (
        "huggingface"
        if settings.image_provider.lower() == "huggingface"
        else "openai"
    )

    if provider == "openai":
        return _generate_with_openai(prompt)
    else:
        return _generate_with_hf(prompt)
