"""Handler for add prompt view submission."""
from logging import Logger
from typing import Any

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt


def add_prompt_view_callback(
    view: Any, ack: Ack, body: Any, client: WebClient, logger: Logger
) -> None:
    """Handle the submission of the add prompt view."""
    try:
        # Acknowledge the view submission
        ack()

        # Extract user ID
        user_id = body["user"]["id"]

        # Extract values from the submitted form
        values = view["state"]["values"]
        title = values["prompt_title_block"]["prompt_title_input"]["value"]
        category = values["prompt_category_block"]["prompt_category_select"]["selected_option"]["value"]
        content = values["prompt_content_block"]["prompt_content_input"]["value"]

        # Save the prompt to the database
        db = next(get_db())
        try:
            prompt = Prompt.create(
                db=db,
                title=title,
                content=content,
                user_id=user_id,
                category=category,
            )
            logger.info("Prompt created: %s", prompt.id)

            # Update the home tab to show the new prompt
            _update_home_tab(client, user_id)

            # Send a confirmation message to the user
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text=f"✅ Your prompt *{title}* has been saved to your library!",
            )
        except Exception:
            logger.exception("Error saving prompt")
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text="❌ There was an error saving your prompt. Please try again.",
            )
    except Exception:
        logger.exception("Error processing add prompt view submission")


def _update_home_tab(client: WebClient, user_id: str) -> None:
    """Update the home tab for the user."""
    from listeners.events.app_home_opened import update_home_tab
    update_home_tab(client, user_id)
