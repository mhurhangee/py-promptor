"""Handler for saving a message as a prompt."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.slack import handle_error
from lib.ui import add_prompt_modal


def save_message_as_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the save message as prompt shortcut."""
    try:
        # Acknowledge the shortcut request
        ack()

        # Get the message text from the body
        message_text = body["message"]["text"]

        # Open a modal for the user to add a prompt, pre-filling the content
        view = add_prompt_modal(initial_content=message_text)

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
            message="Sorry, something went wrong while trying to save this message as a prompt."
        )
