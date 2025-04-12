from typing import Optional

from pydantic import BaseModel


class CoverLetterMetadata(BaseModel):
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
    metadata: Optional[CoverLetterMetadata] = None
    customPrompt: Optional[str] = None
