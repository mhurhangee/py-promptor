"""Handler for deleting a prompt from the library."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.slack import get_prompt_id, get_view_id


def delete_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the delete prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Get the prompt ID
        prompt_id = get_prompt_id(body)

        # If from a modal, get the view ID to properly update it
        view_id = get_view_id(body)

        # Create a confirmation dialog
        view = {
            "type": "modal",
            "callback_id": "delete_prompt_confirmation",
            "private_metadata": str(prompt_id),  # Store the prompt ID in private_metadata
            "title": {"type": "plain_text", "text": "Confirm Deletion", "emoji": True},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Are you sure you want to delete this prompt?*\nThis action cannot be undone."
                    }
                },
            ],
            "submit": {"type": "plain_text", "text": "Delete", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        }

        client.views_update(
            view_id=view_id,
            view=view
        )

    except Exception:
        logger.exception("Error handling delete prompt button")
