"""Handler for delete prompt confirmation view submission."""
from logging import Logger
from typing import Any

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt


def delete_prompt_confirmation_callback(
    view: Any, ack: Ack, body: Any, client: WebClient, logger: Logger
) -> None:
    """Handle the submission of the delete prompt confirmation view."""
    try:
        # Acknowledge the view submission
        ack()

        # Extract user ID
        user_id = body["user"]["id"]

        # Extract prompt ID from private_metadata
        prompt_id = int(view["private_metadata"])

        # Delete the prompt from the database
        db = next(get_db())
        success = Prompt.delete(db, prompt_id)

        if success:
            logger.info("Prompt deleted: %s", prompt_id)

            # Update the home tab to reflect the deletion
            from listeners.events.app_home_opened import update_home_tab
            update_home_tab(client, user_id)

            # Send a confirmation message to the user
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text="✅ Prompt deleted successfully!",
            )
        else:
            logger.warning("Failed to delete prompt: %s", prompt_id)
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text="❌ Failed to delete the prompt. It may have already been deleted.",
            )
    except Exception:
        logger.exception("Error processing delete prompt confirmation")
