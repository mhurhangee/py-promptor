"""Handler for toggling favorite status of a prompt."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import get_prompt_id, get_user_id, get_view_id, handle_error
from lib.ui import prompt_detail_modal
from listeners.events.app_home_opened import update_home_tab


def toggle_favorite_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the toggle favorite button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the prompt ID from the action ID
        prompt_id = get_prompt_id(body)

        # Get the user ID
        user_id = get_user_id(body)

        # Get the view ID to properly update it
        view_id = get_view_id(body)

        # Get the prompt from the database and toggle its favorite status
        db = next(get_db())
        success = Prompt.toggle_favorite(db, prompt_id)

        if success:
            # Get the prompt to update the UI
            prompt = Prompt.get_by_id(db, prompt_id)

            # If the action was triggered from a modal, update the modal
            if view_id and prompt:
                # Create an updated modal view using the modal builder
                view = prompt_detail_modal(prompt)

                try:
                    # Update the modal view
                    client.views_update(
                        view_id=view_id,
                        view=view
                    )
                except Exception as e:
                    logger.warning("Could not update view: %s", e)

            # Update the home tab to reflect the changes
            update_home_tab(client, user_id, logger)

        else:
            # Handle the case where toggling the favorite status failed
            handle_error(
                client=client,
                body=body,
                logger=logger,
                error=Exception("Failed to toggle favorite status"),
                message="Could not update favorite status. Please try again."
            )
    except Exception as e:
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=e,
            message="Could not update favorite status. Please try again."
        )
