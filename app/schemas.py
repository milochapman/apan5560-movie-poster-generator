from pydantic import BaseModel, Field

class PosterRequest(BaseModel):
    summary: str = Field(..., description="Movie plot summary or keywords")
    style_hint: str | None = Field(default=None)

class PosterResponse(BaseModel):
    image_url: str
    prompt: str
