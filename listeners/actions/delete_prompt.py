"""Handler for deleting a prompt from the library."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.slack import get_prompt_id, get_view_id, handle_error
from lib.ui import delete_prompt_confirmation_modal


def delete_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the delete prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Get the prompt ID
        prompt_id = get_prompt_id(body)

        # If from a modal, get the view ID to properly update it
        view_id = get_view_id(body)

        # Create a confirmation dialog using the modal builder
        view = delete_prompt_confirmation_modal(prompt_id)

        client.views_update(
            view_id=view_id,
            view=view
        )

    except Exception as e:
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=e,
            message="Could not prepare the delete confirmation. Please try again."
        )
