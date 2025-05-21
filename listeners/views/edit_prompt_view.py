"""Handler for edit prompt view submission."""
from logging import Logger
from typing import Any

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt


def edit_prompt_view_callback(
    view: Any, ack: Ack, body: Any, client: WebClient, logger: Logger
) -> None:
    """Handle the submission of the edit prompt view."""
    try:
        # Acknowledge the view submission
        ack()

        # Extract user ID
        user_id = body["user"]["id"]

        # Extract prompt ID from private_metadata
        prompt_id = int(view["private_metadata"])

        # Extract values from the submitted form
        values = view["state"]["values"]
        title = values["title_block"]["title_input"]["value"]
        category = values["category_block"]["category_input"]["selected_option"]["value"]
        content = values["content_block"]["content_input"]["value"]

        # Update the prompt in the database
        db = next(get_db())
        try:
            # Get the prompt
            prompt = Prompt.get_by_id(db, prompt_id)

            if not prompt:
                logger.warning("Prompt not found for editing: %s", prompt_id)
                client.chat_postEphemeral(
                    channel=user_id,
                    user=user_id,
                    text="❌ The prompt you're trying to edit could not be found.",
                )
                return

            # Update the prompt
            prompt.title = title
            prompt.category = category
            prompt.content = content
            db.commit()

            logger.info("Prompt updated: %s", prompt_id)

            # Update the home tab to show the updated prompt
            _update_home_tab(client, user_id)

            # Send a confirmation message to the user
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text=f"✅ Your prompt *{title}* has been updated!",
            )
        except Exception:
            logger.exception("Error updating prompt")
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text="❌ There was an error updating your prompt. Please try again.",
            )
    except Exception:
        logger.exception("Error processing edit prompt view submission")


def _update_home_tab(client: WebClient, user_id: str) -> None:
    """Update the home tab for the user."""
    from listeners.events.app_home_opened import update_home_tab
    update_home_tab(client, user_id)
