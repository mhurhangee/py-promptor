"""Handler for filtering prompts by category."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import get_user_id
from lib.ui.prompt_library import get_prompt_library_blocks


def filter_category_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the filter by category selection."""
    try:
        # Acknowledge the action
        ack()

        # Get the user ID
        user_id = get_user_id(body)

        # Get the selected category
        selected_category = body["actions"][0]["selected_option"]["value"]
        selected_text = body["actions"][0]["selected_option"]["text"]["text"]

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
        blocks = get_prompt_library_blocks(user_id, show_add_button=True, filtered_prompts=prompts)

        # Update the home tab with the filtered prompts
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": blocks,
            },
        )

    except Exception:
        logger.exception("Error handling category filter")
