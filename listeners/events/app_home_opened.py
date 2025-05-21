from logging import Logger
from typing import Optional

from slack_sdk import WebClient

from lib.ui.prompt_library import get_prompt_library_blocks


def app_home_opened_callback(client: WebClient, event: dict, logger: Logger) -> None:
    """Handle the app_home_opened event."""
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return

    try:
        # Update the home tab with the user's prompts
        update_home_tab(client, event["user"], logger)
    except Exception:
        logger.exception("Error publishing home tab")


def update_home_tab(client: WebClient, user_id: str, logger: Optional[Logger] = None) -> None:
    """Update the home tab for the user with their saved prompts."""
    try:
        # Get the prompt library blocks for the home tab
        blocks = get_prompt_library_blocks(user_id)

        # Publish the view
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": blocks,
            },
        )
    except Exception:
        if logger:
            logger.exception("Error updating home tab")
