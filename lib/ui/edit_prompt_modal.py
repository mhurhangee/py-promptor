from typing import Any, Dict

from lib.ui.add_prompt_modal import add_prompt_modal


def edit_prompt_modal(prompt: Any) -> Dict[str, Any]:
    """
    Create a modal view for editing a prompt.

    Args:
        prompt: A Prompt object with attributes id, title, category, content
    """
    # Get tags if they exist
    tags = ""
    if hasattr(prompt, "tags"):
        tags = getattr(prompt, "tags", "")

    # Reuse the add_prompt_modal with different title and callback_id
    modal_view = add_prompt_modal(
        initial_content=prompt.content,
        initial_title=prompt.title,
        initial_category=str(prompt.category) if prompt.category else None,
        initial_tags=tags,
        private_metadata=str(prompt.id)
    )

    # Update the modal properties for editing
    modal_view["title"]["text"] = "Edit Prompt"
    modal_view["callback_id"] = "edit_prompt_view"
    modal_view["submit"]["text"] = "💾 Save Changes"

    return modal_view
