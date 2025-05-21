from typing import Any, Dict

from lib.slack.blocks import actions, button, context_text, modal, section
from lib.ui.prompt_library import create_prompt_metadata_text


def prompt_detail_modal(prompt: Any) -> Dict[str, Any]:
    """
    Create a modal view for displaying prompt details.

    Args:
        prompt: A Prompt object with attributes id, title, category, content, is_favorite, created_at
    """
    # Use the reusable metadata function for consistency
    metadata_text = create_prompt_metadata_text(prompt)

    # Format the prompt content as a code block for better visibility
    content = str(prompt.content).strip()
    formatted_content = f"```\n{content}\n```"

    blocks = [
        context_text(metadata_text),
        section(formatted_content),
        actions([
            button("🧪 Test it", f"use_prompt:{prompt.id}", style="primary"),
            button("💔 Unfavorite" if prompt.is_favorite else "⭐ Favorite", f"toggle_favorite:{prompt.id}"),
            button("✏️ Edit", f"edit_prompt:{prompt.id}"),
            button("🗑️ Delete", f"delete_prompt:{prompt.id}", style="danger"),
        ]),

    ]

    # Truncate title to 24 characters (leaving room for ellipsis if needed)
    max_title_length = 24
    title = prompt.title
    if len(title) > max_title_length:
        title = title[:max_title_length] + "…"

    return modal(
        title=title,
        blocks=blocks,
        callback_id="prompt_details_view",
    )
