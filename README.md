# APAN 5560 – Movie Poster Generator (Stable Diffusion XL + FastAPI)

This project exposes a simple FastAPI server that turns a **movie plot summary** into a **poster-style image** using **Stable Diffusion XL** via the Hugging Face Inference API.

- Backend: FastAPI
- Model: `stabilityai/stable-diffusion-xl-base-1.0`
- Provider: Hugging Face Inference API (`hf-inference`)
- Deployment: Docker (FastAPI + Uvicorn)

---

## 1. Setup (local, no Docker)

```bash
cd apan5560-movie-poster-generator
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a **Hugging Face token**:

1. Go to https://huggingface.co/settings/tokens
2. Create a token with at least **read** permissions
3. Copy the token value (starts with `hf_...`)

Then update `.env`:

```env
IMAGE_PROVIDER=huggingface
HF_API_KEY=hf_your_token_here
```

Start the API server:

```bash
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Generate a poster:

```bash
curl -X POST "http://127.0.0.1:8000/generate_poster" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "A time traveler fights a corrupted AI system in the future",
    "style_hint": "cinematic, sci-fi, neon lighting"
  }'
```

The response JSON contains a `image_url` field with a **data URL** (base64 PNG).  
You can paste this into a browser or save it via a small helper script.

---

## 2. Running with Docker

Build:

```bash
docker build -t apan5560-movie-poster-generator -f docker/Dockerfile .
```

Run (Linux/macOS bash):

```bash
docker run --rm -p 8000:8000 \
  -e IMAGE_PROVIDER=huggingface \
  -e HF_API_KEY=hf_your_token_here \
  apan5560-movie-poster-generator
```

Then you can call the same `/generate_poster` endpoint from your host.

---

## 3. API Overview

### `GET /health`

Simple health check. Returns `{"status": "ok"}` if the server is running.

### `POST /generate_poster`

Request body:

```json
{
  "summary": "Short description of the movie plot",
  "style_hint": "Optional style hint, like 'cyberpunk, neon, high contrast'"
}
```

Response body:

```json
{
  "image_url": "data:image/png;base64,...",
  "prompt": "Full text prompt actually sent to the model"
}
```

This design makes it easy to integrate with a front-end: just set the `src` of an `<img>` tag to `image_url`.

---

## 4. Project Structure

- `app/main.py` – FastAPI app and HTTP endpoints
- `app/poster_generator.py` – Prompt building + calls to OpenAI / Hugging Face
- `app/config.py` – Settings and environment variables
- `app/schemas.py` – Pydantic models for request/response
- `docker/Dockerfile` – Docker image definition
- `tests/test_api.py` – Basic health-check test
- `report/` – Outlines for the final report and slides

---

## 5. Notes for the Class Project

- **Generative AI technique**: Text-to-image generation with Stable Diffusion XL through Hugging Face Inference.
- **Value-add**: This API wraps SDXL with:
  - Movie-specific prompt engineering
  - A clean, reproducible FastAPI + Docker interface
  - Clear separation of configuration (env vars) vs. code
- **Extension ideas**:
  - Add multiple styles (horror, romance, sci-fi) as presets
  - Accept additional fields (main character, setting, mood) and mix them into the prompt
  - Build a small web UI that calls this API and shows poster thumbnails.

