"""Schema for the metadata agent response."""

from pydantic import BaseModel, Field


class MetadataSchema(BaseModel):
    """Schema for metadata generation response."""

    title: str = Field(
        ...,
        description="A concise, descriptive title for the prompt. Should be clear and under 25 characters.",
    )

    category: str = Field(
        ...,
        description="The most appropriate category for this prompt from the available options.",
    )

    tags: str = Field(
        ...,
        description="2-3 relevant single-word tags for the prompt, comma-separated. These should help with organization and searchability.",
    )
