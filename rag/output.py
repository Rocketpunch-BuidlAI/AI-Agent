from pydantic import BaseModel, Field


class UsedCoverLetter(BaseModel):
    id: str = Field(..., description="ID of the used Source")
    contributions: int = Field(
        ..., description="Percentage of contributions from the used cover letter"
    )


class EditResponseFormatter(BaseModel):
    text: str = Field(..., description="Created Coverletter text, Do not include sources")
    used_sources: list[UsedCoverLetter] = Field(
        ..., description="List of used sources with contributions"
    )
