from pydantic import BaseModel, Field


class UsedCoverLetter(BaseModel):
    id: str = Field(..., description="ID of the used Source")
    contributions: int = Field(
        ..., description="Percentage of contributions from the used cover letter"
    )


class EditResponseFormatter(BaseModel):
    text: str = Field(..., description="Text for Cover Letter")
    used_sources: list[UsedCoverLetter] = Field(
        ..., description="List of used sources with contributions"
    )
