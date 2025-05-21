from typing import Any, Dict

from .confirmation_modal import confirmation_modal


def delete_prompt_confirmation_modal(prompt_id: int) -> Dict[str, Any]:
    """Create a confirmation modal for deleting a prompt."""
    return confirmation_modal(
        title="Confirm Deletion",
        text="*Are you sure you want to delete this prompt?*\nThis action cannot be undone.",
        callback_id="delete_prompt_confirmation",
        confirm_text="Delete",
        private_metadata=str(prompt_id),
    )
