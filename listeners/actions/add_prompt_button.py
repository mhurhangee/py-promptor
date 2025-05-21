"""Handler for adding a new prompt."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.slack import handle_error
from lib.ui import add_prompt_modal


def add_prompt_button_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the add prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Create the modal view using the modal builder
        view = add_prompt_modal()

        client.views_open(
            trigger_id=body["trigger_id"],
            view=view
        )
    except Exception as e:
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=e,
            message="Sorry, something went wrong while adding the prompt."
        )
