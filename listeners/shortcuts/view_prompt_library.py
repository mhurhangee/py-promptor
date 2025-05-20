"""View prompt library shortcut handler."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.ui.prompt_library import get_prompt_library_blocks


def view_prompt_library_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the view prompt library shortcut."""
    try:
        # Acknowledge the shortcut request
        ack()

        # Get the user ID
        user_id = body["user"]["id"]

        # Get the prompt library blocks (only show add button, not modal button)
        blocks = get_prompt_library_blocks(user_id, show_add_button=True, show_modal_button=False)

        # Open the modal
        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "prompt_library_modal",
                "title": {"type": "plain_text", "text": "Prompt Library"},
                "blocks": blocks,
                "close": {"type": "plain_text", "text": "Close", "emoji": True}
            }
        )
    except Exception:
        logger.exception("Error opening prompt library modal")
