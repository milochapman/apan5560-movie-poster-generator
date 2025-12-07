# APAN 5560 – Movie Poster Generator
A text-to-image generation system using FastAPI, HuggingFace/OpenAI APIs, and structured prompt engineering.

## Overview
This project implements an end-to-end movie poster generation pipeline. The user provides a short story summary and an optional style hint. The system transforms the input into an optimized cinematic prompt and generates a poster image using a text-to-image model.

The repository does not include any API keys. All sensitive information is stored locally in a `.env` file as required by course security guidelines.

## Repository Structure
```
apan5560-movie-poster-generator/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── poster_generator.py
│   ├── prompt_builder.py
│   └── schemas.py
│
├── tests/
├── report/
├── generate_all_poster.py
├── save_poster.py
├── requirements.txt
└── README.md
```

## API Key Handling
API keys must be stored in a local `.env` file. This file is excluded via `.gitignore` and must be created manually.

Example `.env`:
```
IMAGE_PROVIDER=huggingface
HF_API_KEY=your_token_here
HF_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

## Installation
### 1. Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Start the API server
```
uvicorn app.main:app --reload --port 8000
```

## Usage
### Example JSON request:
```json
{
  "summary": "A mysterious force rises from an ancient planet.",
  "style_hint": "sci-fi, dramatic lighting"
}
```

### Saving Posters Locally
Large base64 images may decode slowly in browsers.  
The project includes `save_poster.py`, which downloads and saves the generated image locally.

Example usage:
```
python save_poster.py
```

An output file `poster.png` will be written to the project directory.

## Testing
```
pytest
```

## Notes on Model Performance
Large models such as SDXL may generate high-resolution outputs that cause slow browser rendering. For this reason, the `save_poster.py` script is provided to reliably save images without rendering delays.

## Academic Integrity & Security
- No API keys are included in this repository.
- `.env` and `.venv` are excluded from version control.
- Keys are sent privately to the instructor for grading.
