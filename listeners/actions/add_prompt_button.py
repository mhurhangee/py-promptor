"""Handler for the Add New Prompt button action."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from listeners.shortcuts.add_prompt import add_prompt_shortcut_callback


def add_prompt_button_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the add prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Reuse the shortcut callback to open the modal
        add_prompt_shortcut_callback(body, ack, client, logger)
    except Exception:
        logger.exception("Error handling add prompt button")
