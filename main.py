from fastapi import Body, FastAPI
from pydantic import BaseModel

from rag import enhance_resume

app = FastAPI()


class CoverLetterIn(BaseModel):
    text: str
    company: str


class ResumeIn(BaseModel):
    text: str
    target_company: str


@app.post("/upload")
def upload_cover_letter(data: CoverLetterIn):
    # load_resumes_to_pinecone(data.text, metadata={"company": data.company})
    return {"status": "success", "message": "Cover letter uploaded and embedded."}


@app.post("/enhance-resume")
def enhance(data: ResumeIn):
    result = enhance_resume(data.text, data.target_company)
    return result


@app.get("/status")
def status():
    return {"status": "ok"}
