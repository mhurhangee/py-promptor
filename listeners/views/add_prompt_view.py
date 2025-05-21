"""Handler for add prompt view submission."""
import json
from logging import Logger
from typing import Any

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import handle_error

# Constants
MAX_TITLE_LENGTH = 50
MAX_LOG_CONTENT_LENGTH = 100


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
        logger.info("Form values: %s", values)

        # Extract content (required field)
        content = values["content_block"]["content_input"]["value"]
        logger.info("Content: %s", content[:MAX_LOG_CONTENT_LENGTH] + "..." if len(content) > MAX_LOG_CONTENT_LENGTH else content)

        # Check if we have suggested metadata in private_metadata
        suggested_metadata = {}
        if view["private_metadata"]:
            try:
                suggested_metadata = json.loads(view["private_metadata"])
                logger.info("Found suggested metadata: %s", suggested_metadata)
            except json.JSONDecodeError:
                logger.warning("Failed to parse private_metadata as JSON")

        # Get optional fields (title, category, tags)
        title_input = values["title_block"]["title_input"]
        logger.info("Title input: %s", title_input)
        title = title_input.get("value", "") if title_input.get("value") is not None else ""

        # If title is empty and we have a suggested title, use that
        if not title and "suggested_title" in suggested_metadata:
            title = suggested_metadata["suggested_title"]
            logger.info("Using suggested title: %s", title)
        logger.info("Final title: %s", title)

        # Get tags (from form or suggested)
        tags_input = values["tags_block"]["tags_input"]
        logger.info("Tags input: %s", tags_input)
        tags = tags_input.get("value", "") if tags_input.get("value") is not None else ""

        # If tags is empty and we have suggested tags, use those
        if not tags and "suggested_tags" in suggested_metadata:
            tags = suggested_metadata["suggested_tags"]
            logger.info("Using suggested tags: %s", tags)
        logger.info("Final tags: %s", tags)

        # Get category if selected
        category = None
        category_input = values["category_block"]["category_input"]
        logger.info("Category input: %s", category_input)

        # Check for selected_option in category_input
        if category_input and "selected_option" in category_input and category_input["selected_option"]:
            category = category_input["selected_option"]["value"]

        # If category is None and we have a suggested category, use that
        if category is None and "suggested_category" in suggested_metadata:
            category = suggested_metadata["suggested_category"]
            logger.info("Using suggested category: %s", category)
        logger.info("Final category: %s", category)

        # Save the prompt to the database
        db = next(get_db())
        # If title is empty, use the first few chars of content as title
        if not title:
            title = content[:MAX_TITLE_LENGTH] + ("..." if len(content) > MAX_TITLE_LENGTH else "")

        prompt = Prompt.create(
                db=db,
                content=content,
                user_id=user_id,
                title=title,
                category=category,
                tags=tags,
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
        logger.exception("Error processing add prompt view submission")
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=Exception("Error processing add prompt view submission"),
            message="Sorry, something went wrong while adding the prompt."
        )


def _update_home_tab(client: WebClient, user_id: str) -> None:
    """Update the home tab for the user."""
    from listeners.events.app_home_opened import update_home_tab
    update_home_tab(client, user_id)
