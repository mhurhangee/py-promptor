"""Metadata agent for generating prompt metadata."""
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from config.categories import DEFAULT_CATEGORIES
from config.settings import AI_MODEL

from .metadata_schema import MetadataSchema


def create_metadata_agent(session_id: str = "") -> Agent:
    """
    Create an agent specifically for generating metadata for prompts.

    Args:
        session_id: Optional session ID for tracking conversations

    Returns:
        An Agno agent configured for metadata generation
    """
    # Create a comma-separated list of available categories
    available_categories = ", ".join(f'"{cat}"' for cat in DEFAULT_CATEGORIES)

    # Custom system message for metadata generation
    system_message = f"""You are a metadata specialist for an AI prompt library.
Your job is to analyze prompt content and generate appropriate metadata.

When given a prompt, you will:
1. Generate a concise, descriptive title (max 50 chars)
2. Select the most appropriate category from: {available_categories}
3. Generate 3-5 relevant tags (comma-separated)

Be precise, accurate, and helpful. Focus on the main purpose and content of the prompt.
"""

    return Agent(
        model=OpenAIChat(
            id=AI_MODEL["id"],
            temperature=0.3,  # Lower temperature for more consistent metadata
            max_completion_tokens=200,  # Metadata is short, so we don't need many tokens
        ),
        session_id=session_id,
        markdown=False,  # Metadata doesn't need markdown
        system_message=system_message,
        add_history_to_messages=False,  # No need for history in metadata generation
        response_model=MetadataSchema,
        use_json_mode=True,
    )
