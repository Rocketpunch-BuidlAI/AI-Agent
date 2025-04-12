from math import e

from fastapi import Body, FastAPI
from pydantic import BaseModel

from rag.rag import generate_cover_letter, load_coverletter

app = FastAPI()


class UsedCoverLetter(BaseModel):
    id: str
    contributions: int


class EditResponse(BaseModel):
    enhanced_cover_letter: str
    used_sources: list[UsedCoverLetter]


class PublishCoverLetterMetadata(BaseModel):
    id: str
    text: str


class CreateCoverLetterReq(BaseModel):
    text: str


@app.post("/upload")
async def upload_cover_letter(
    text: str = Body(
        ...,
        embed=True,
    ),
    id: str = Body(
        ...,
        embed=True,
    ),
    role: str = Body(
        ...,
        embed=True,
    ),
    experience: str = Body(
        ...,
        embed=True,
        example="junior, senior",
    ),
):
    load_coverletter(text, id, role, experience)

    return {"status": "success", "message": "Cover letter uploaded and embedded."}


@app.post("/edit")
def create(
    text: str = Body(
        ...,
        embed=True,
    ),
):
    return generate_cover_letter(
        text="",
        prompt="",
    )


@app.get("/status")
def status():
    return {"status": "ok"}
