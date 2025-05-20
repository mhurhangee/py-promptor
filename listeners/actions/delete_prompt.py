"""Handler for deleting a prompt from the library."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt


def delete_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the delete prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the prompt ID from the action_id
        action_id = body["actions"][0]["action_id"]
        prompt_id = int(action_id.split(":")[-1])

        # Get the user ID
        user_id = body["user"]["id"]

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
        logger.exception("Error handling delete prompt button")
