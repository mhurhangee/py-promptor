"""Handler for filtering prompts by category."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from listeners.events.app_home_opened import update_home_tab


def filter_category_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the filter by category selection."""
    try:
        # Acknowledge the action
        ack()

        # Get the user ID
        user_id = body["user"]["id"]

        # Get the selected category
        selected_category = body["actions"][0]["selected_option"]["value"]

        # Store the selected category in user state (this would be expanded in a real implementation)
        # For now, we'll just update the home tab
        logger.info("User %s filtered prompts by category: %s", user_id, selected_category)

        # Update the home tab with the filtered prompts
        # In a real implementation, we would pass the filter to get_prompt_library_blocks
        update_home_tab(client, user_id, logger)
        
    except Exception:
        logger.exception("Error handling category filter")
