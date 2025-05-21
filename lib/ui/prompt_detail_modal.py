from typing import Any, Dict

from lib.slack.blocks import actions, button, context_text, divider, modal, section


def prompt_detail_modal(prompt: Any) -> Dict[str, Any]:
    """
    Create a modal view for displaying prompt details.

    Args:
        prompt: A Prompt object with attributes id, title, category, content, is_favorite, created_at
    """
    blocks = [
        section(f"*Category:* {prompt.category}"),
        divider(),
        section(str(prompt.content)),
        divider(),
        actions([
            button("Use", f"use_prompt:{prompt.id}", style="primary"),
            button("★ Unfavorite" if prompt.is_favorite else "☆ Favorite", f"toggle_favorite:{prompt.id}"),
            button("✏️ Edit", f"edit_prompt:{prompt.id}"),
            button("🗑️ Delete", f"delete_prompt:{prompt.id}", style="danger"),
        ]),
        context_text(f"Created: {prompt.created_at.strftime('%Y-%m-%d')}")
    ]

    return modal(
        title=prompt.title,
        blocks=blocks,
        callback_id="prompt_details_view",
    )
