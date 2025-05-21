from typing import Dict

from lib.db.models import Prompt
from lib.slack.blocks import context_text


def create_prompt_metadata_text(prompt: Prompt) -> str:
    """Create a formatted metadata string for a prompt.

    This is a utility function that can be used across different UI components.

    Args:
        prompt: The prompt object containing metadata

    Returns:
        A formatted string with category, tags, and creation date
    """
    # Format the category
    category_text = f"*{prompt.category or 'None'}*"

    # Format the tags if they exist
    tags_text = ""
    if hasattr(prompt, "tags"):
        tags = getattr(prompt, "tags", "")
        if tags and str(tags).strip():
            tags_text = f"🏷️ *{tags}*"

    # Format the creation date
    date_text = f"📅 {prompt.created_at.strftime('%Y-%m-%d')}"

    return f"{date_text} {category_text} {tags_text}"


def create_prompt_context_block(prompt: Prompt) -> Dict:
    """Create a context block with prompt metadata."""
    return context_text(create_prompt_metadata_text(prompt))
