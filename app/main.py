from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PosterRequest, PosterResponse
from .poster_generator import generate_poster

app = FastAPI(title="Movie Poster Generator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate_poster", response_model=PosterResponse)
def generate(request: PosterRequest):
    try:
        return generate_poster(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
