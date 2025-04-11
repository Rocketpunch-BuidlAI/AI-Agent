import json

from fastapi import Body, FastAPI, File, Form, UploadFile
from pydantic import BaseModel

from rag import enhance_resume

app = FastAPI()


class UsedCoverLetter(BaseModel):
    id: str
    contributions: int


class EditResponse(BaseModel):
    enhanced_cover_letter: str
    used_sources: list[UsedCoverLetter]


@app.post("/upload")
async def upload_cover_letter(
    coverletter: UploadFile = File(...),
    metadata: str = Form(..., description="JSON string metadata for the cover letter"),
):
    content = await coverletter.read()
    text = content.decode("utf-8")

    try:
        metadata_dict = json.loads(metadata)
        company = metadata_dict.get("company")
    except json.JSONDecodeError:
        return {"status": "error", "message": "Invalid metadata format"}

    # load_resumes_to_pinecone(text, metadata={"company": company})
    return {"status": "success", "message": "Cover letter uploaded and embedded."}


@app.post("/edit", response_model=EditResponse)
def enhance(
    original_cover_letter: UploadFile = File(..., description="Original cover letter from user"),
    metadata: str = Form(..., description="JSON string metadata for the cover letter"),
):
    return {
        "enhanced_cover_letter": "Enhanced cover letter content goes here.",
        "used_sources": [
            {
                "id": "source_id",
                "contributions": 60,
            },
            {
                "id": "source_id",
                "contributions": 40,
            },
        ],
    }


@app.get("/status")
def status():
    return {"status": "ok"}
