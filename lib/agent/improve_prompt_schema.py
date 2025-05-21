"""Schema for the improve prompt agent response."""
from pydantic import BaseModel, Field


class ImprovePromptSchema(BaseModel):
    """Schema for the improve prompt agent response."""

    improved_prompt: str = Field(
        ...,
        description="The improved version of the original prompt. This should be a complete replacement that is clearer, more effective, and better structured.",
    )

    reasoning: str = Field(
        ...,
        description="Explanation of how and why the prompt was improved. Include specific changes made and the rationale behind them.",
    )
