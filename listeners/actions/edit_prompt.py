"""Handler for editing a prompt from the library."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import get_prompt_id, get_view_id, handle_error, send_error_eph
from lib.ui import edit_prompt_modal


def edit_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the edit prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the prompt ID
        prompt_id = get_prompt_id(body)

        # Get the prompt from the database
        db = next(get_db())
        prompt = Prompt.get_by_id(db, prompt_id)

        if not prompt:
            send_error_eph(client, body, "Prompt not found")
            return

        # Get the view ID to update the modal
        view_id = get_view_id(body)

        # Create the modal view using the modal builder
        view = edit_prompt_modal(prompt)

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
            message="Sorry, something went wrong while editing the prompt."
        )
