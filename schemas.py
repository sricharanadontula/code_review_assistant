
from pydantic import BaseModel, Field


class ReviewResult(BaseModel):
    identified_issues: list[str] = Field(
        description="Problems found in the submitted code"
    )

    improvement_suggestions: list[str] = Field(
        description="Practical suggestions to improve the code"
    )

    code_quality_level: str = Field(
        description="Overall code quality: Low, Medium, or High"
    )

    review_summary: str = Field(
        description="A brief summary of the code review"
    )
