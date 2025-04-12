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
    result = generate_cover_letter(
        selfIntroduction=data.selfIntroduction,
        motivation=data.motivation,
        relevantExperience=data.relevantExperience,
        futureAspirations=data.futureAspirations,
        metadata=data.metadata.dict() if data.metadata else {},  # type: ignore
        prompt=data.customPrompt or "",
    )
    
    return result


@app.post("/coverletters")
def get_coverletter(
    role: str = Body(
        embed=True,
    ),
    experience: str = Body(),
):
    result = retrieve(experience, role)
    
    # source_id 필드가 178 이상이면서 192가 아닌 항목만 포함
    if isinstance(result, list):
        filtered_results = [doc for doc in result if hasattr(doc, 'source_id') and int(doc.source_id) >= 178 and int(doc.source_id) != 192]
        return filtered_results
    
    # 다른 형식의 응답일 경우 원본 데이터를 그대로 반환
    return result


@app.get("/status")
def status():
    return {"status": "ok"}
