from fastapi import Body, FastAPI
from pydantic import BaseModel

import rag.configs
from rag.rag import enhance_resume, load_coverletter

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
):
    load_coverletter(coverletter=text, metadata={"id": id})

    return {"status": "success", "message": "Cover letter uploaded and embedded."}


@app.post("/edit")
def create(
    text: str = Body(
        ...,
        embed=True,
    ),
):
    return enhance_resume(
        user_resume_text="",
    )


@app.get("/status")
def status():
    return {"status": "ok"}
