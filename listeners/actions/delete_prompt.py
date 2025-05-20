"""Handler for deleting a prompt from the library."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient


def delete_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the delete prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the prompt ID from the action_id
        action_id = body["actions"][0]["action_id"]
        prompt_id = int(action_id.split(":")[-1])

        # We don't need the user ID here as we're just showing a confirmation dialog
        # The actual deletion will happen in the view submission handler

        # Check if this action was triggered from within a modal
        is_from_modal = body.get("container", {}).get("type") == "view"

        # If from a modal, get the view ID to properly update it
        view_id = body.get("container", {}).get("view_id") if is_from_modal else None
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

        # If triggered from the detail view modal, update that view
        if is_from_modal and view_id:
            try:
                client.views_update(
                    view_id=view_id,
                    view=view
                )
            except Exception as e:
                logger.warning("Could not update view, falling back to views_open: %s", e)
                client.views_open(
                    trigger_id=body["trigger_id"],
                    view=view
                )
        else:
            # Otherwise, open a new modal
            client.views_open(
                trigger_id=body["trigger_id"],
                view=view
            )
    except Exception:
        logger.exception("Error handling delete prompt button")
