"""Handler for viewing prompt details."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import get_prompt_id, handle_error, send_error_eph
from lib.ui import prompt_detail_modal


def view_prompt_details_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the view prompt details button click."""
    try:
        # Acknowledge the button click
        ack()

        # Get prompt ID and user id
        prompt_id = get_prompt_id(body)

        # Get the prompt from the database
        db = next(get_db())
        prompt = Prompt.get_by_id(db, prompt_id)

        if not prompt:
            send_error_eph(client, body, "Sorry, that prompt could not be found.")
            return

        # Create the modal view with all action buttons using the modal builder
        view = prompt_detail_modal(prompt)

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
            message="Sorry, something went wrong while viewing the prompt details."
        )
