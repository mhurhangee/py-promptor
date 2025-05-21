"""Add prompt shortcut handler."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.ui import add_prompt_modal


def add_prompt_shortcut_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the add prompt shortcut."""
    try:
        # Acknowledge the shortcut request
        ack()

        # Open a modal for the user to add a prompt using the modal builder
        client.views_open(
            trigger_id=body["trigger_id"],
            view=add_prompt_modal()
        )
    except Exception:
        logger.exception("Error opening add prompt modal")
