from typing import Optional
from math import e

from fastapi import Body, FastAPI
from pydantic import BaseModel

from rag.rag import generate_cover_letter, load_coverletter, retrieve

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


class Metadata(BaseModel):
    targetCompany: str
    department: str
    position: str
    experience: str
    skills: str


class CoverLetterData(BaseModel):
    selfIntroduction: str
    motivation: str
    relevantExperience: str
    futureAspirations: str
    metadata: Optional[Metadata] = None
    customPrompt: Optional[str] = None


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
    data: CoverLetterData = Body(...),
):
    return generate_cover_letter(
        selfIntroduction=data.selfIntroduction,
        motivation=data.motivation,
        relevantExperience=data.relevantExperience,
        futureAspirations=data.futureAspirations,
        metadata=data.metadata.dict() if data.metadata else {},  # type: ignore
        prompt=data.customPrompt or "",
    )


@app.post("/coverletters")
def get_coverletter(
    role: str = Body(
        embed=True,
    ),
    experience: str = Body(),
):
    return retrieve(experience, role)


@app.get("/status")
def status():
    return {"status": "ok"}
