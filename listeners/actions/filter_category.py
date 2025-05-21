"""Handler for filtering prompts by category."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import get_user_id, handle_error, send_error_eph
from lib.ui.prompt_library import get_prompt_library_blocks


def filter_category_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the filter by category selection."""
    try:
        # Acknowledge the action
        ack()

        # Get the user ID
        user_id = get_user_id(body)

        # Get the selected category safely
        actions = body.get("actions", [])
        if not actions:
            send_error_eph(client, body, "No category selection found.")
            return

        selected_option = actions[0].get("selected_option", {})
        if not selected_option:
            send_error_eph(client, body, "No category selection found.")
            return

        selected_category = selected_option.get("value", "all")
        selected_text = selected_option.get("text", {}).get("text", "All")

        # Log the selection
        logger.info("User %s filtered prompts by: %s", user_id, selected_text)

        # Get prompts based on the filter
        db = next(get_db())

        # Handle different filter types
        if selected_category == "all":
            # Show all prompts
            prompts = Prompt.get_all_by_user(db, user_id)
        elif selected_category == "favorites":
            # Show only favorites
            prompts = Prompt.get_all_by_user(db, user_id, favorites_only=True)
        else:
            # Filter by category
            prompts = db.query(Prompt).filter(
                Prompt.user_id == user_id,
                Prompt.category == selected_category
            ).all()

        # Create blocks with filtered prompts
        blocks = get_prompt_library_blocks(user_id, filtered_prompts=prompts)

        # Update the home tab with the filtered prompts
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": blocks,
            },
        )

    except Exception as e:
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=e,
            message="Sorry, something went wrong while filtering prompts."
        )
