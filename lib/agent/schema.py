from typing import List, Optional

from pydantic import BaseModel, Field


class ResponseSchema(BaseModel):
    thread_title: str = Field(
        ...,
        description="A short, descriptive title for the entire thread. It should summarize the topic clearly and include a relevant emoji at the beginning.",
    )

    response_title: str = Field(
        ...,
        description="A concise, engaging title for the current response. It should reflect the main idea of the message and include an emoji at the start.",
    )

    response: str = Field(
        ...,
        description="Your main response to the user's message. Use markdown for structure and clarity, and include emojis to keep it engaging. Be educational, friendly, and adapt to the user's level of expertise.",
    )

    follow_ups: Optional[List[str]] = Field(
        None,
        max_length=4,
        description="A list of follow-up prompts (maximum 4) to keep the conversation going. Optional but helpful for promoting curiosity. Each item should be a potential follow-up question the user might ask next, written from the user's perspective. Start with a relevant emoji.",
    )
