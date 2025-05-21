from typing import Any, Dict

from lib.slack.blocks import modal, section


def confirmation_modal(
    title: str,
    text: str,
    callback_id: str,
    confirm_text: str = "Confirm",
    private_metadata: str = "",
) -> Dict[str, Any]:
    """Create a confirmation modal."""
    blocks = [section(text)]
    return modal(
        title=title,
        blocks=blocks,
        callback_id=callback_id,
        submit_text=confirm_text,
        private_metadata=private_metadata,
    )
