"""Handler for the View as Modal button action."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from listeners.shortcuts.view_prompt_library import view_prompt_library_callback


def view_prompts_modal_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the view prompts modal button click."""
    try:
        # Acknowledge the button click
        ack()

        # Reuse the view_prompt_library_callback to open the modal
        view_prompt_library_callback(body, ack, client, logger)
    except Exception:
        logger.exception("Error handling view prompts modal button")
