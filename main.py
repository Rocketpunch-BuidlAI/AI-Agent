import json

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")


from fastapi import Body, FastAPI, File, Form, UploadFile
from pydantic import BaseModel

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


@app.post("/upload")
async def upload_cover_letter(
    coverletter: UploadFile = File(...),
    metadata: str = Form(
        ...,
        description="JSON string metadata for the cover letter {id: <str>}",
        example='{"id": "12345"}',
    ),
):
    content = await coverletter.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as e:
        return {"status": "error", "message": f"Failed to decode content: {str(e)}"}

    try:
        meta = PublishCoverLetterMetadata(**json.loads(metadata))
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid metadata format"}

    load_coverletter(coverletter=text, metadata=meta.model_dump())
    return {"status": "success", "message": "Cover letter uploaded and embedded."}


@app.post("/edit")
def enhance(
    original_cover_letter: UploadFile = File(..., description="Original cover letter from user"),
    metadata: str = Form(..., description="JSON string metadata for the cover letter"),
):
    return enhance_resume(
        user_resume_text="",
    )


@app.get("/status")
def status():
    return {"status": "ok"}
