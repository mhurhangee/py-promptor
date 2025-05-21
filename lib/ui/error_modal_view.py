from typing import Any, Dict

from lib.slack.blocks import modal, section


def error_modal_view(error_message: str) -> Dict[str, Any]:
    """Create an error modal view."""
    blocks = [section(f"❌ *Error:* {error_message}")]
    return modal(
        title="Error",
        blocks=blocks,
        callback_id="error_modal",
        private_metadata=error_message,
    )
