"""Modal for displaying AI-generated responses to prompts."""
from typing import Any, Dict

from lib.slack.blocks import divider, header, modal, section


def prompt_result_modal(
    prompt_title: str,
    prompt_content: str,
    response_title: str,
    response_content: str,
) -> Dict[str, Any]:
    """
    Create a modal view for displaying AI-generated responses to prompts.

    Args:
        prompt_title: The title of the original prompt
        prompt_content: The content of the original prompt
        response_title: The title for the AI response section
        response_content: The AI-generated response content
    """
    blocks = [
        header(prompt_title),
        section(f"*Original Prompt:*\n_{prompt_content}_"),
        divider(),
        section(f"*{response_title}*" if response_title else "*Response:*"),
        section(response_content),
    ]

    return modal(
        title="AI Response",
        blocks=blocks,
        callback_id="prompt_result_view",
    )
