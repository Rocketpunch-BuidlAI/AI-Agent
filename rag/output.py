from pydantic import BaseModel, Field


class UsedCoverLetter(BaseModel):
    id: str = Field(..., description="ID of the used Source")
    contributions: int = Field(
        ..., description="Percentage of contributions from the used cover letter"
    )


class EditResponseFormatter(BaseModel):
    enhanced_cover_letter: str = Field(..., description="Enhanced cover letter content")
    used_sources: list[UsedCoverLetter] = Field(
        ..., description="List of used sources with contributions"
    )
