"""View prompt library shortcut handler."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from listeners.events.app_home_opened import update_home_tab


def view_prompt_library_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the view prompt library shortcut."""
    try:
        # Acknowledge the shortcut request
        ack()

        # Get the user ID
        user_id = body["user"]["id"]

        # Update the home tab to show the prompt library
        update_home_tab(client, user_id, logger)

        # Send an ephemeral message to guide the user
        client.chat_postEphemeral(
            channel=body.get("channel", {}).get("id") or user_id,  # Use channel if available, otherwise DM
            user=user_id,
            text="✨ Your prompt library is ready! Check the Home tab of this app to view and manage your prompts."
        )
    except Exception:
        logger.exception("Error redirecting to prompt library")
