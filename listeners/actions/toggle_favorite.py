"""Handler for toggling favorite status of a prompt."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from listeners.events.app_home_opened import update_home_tab


def toggle_favorite_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the toggle favorite button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the prompt ID from the action ID
        action_id = body["actions"][0]["action_id"]
        prompt_id = int(action_id.split(":")[1])

        # Get the user ID
        user_id = body["user"]["id"]

        # Check if this action was triggered from within a modal
        is_from_modal = body.get("container", {}).get("type") == "view"

        # If from a modal, get the view ID to properly update it
        view_id = body.get("container", {}).get("view_id") if is_from_modal else None

        # Get the prompt from the database and toggle its favorite status
        db = next(get_db())
        success, is_favorite = Prompt.toggle_favorite(db, prompt_id)

        if success:
            # Get the prompt to update the UI
            prompt = Prompt.get_by_id(db, prompt_id)

            # If the action was triggered from a modal, update the modal
            if is_from_modal and view_id and prompt:
                # Create an updated modal view
                view = {
                    "type": "modal",
                    "callback_id": "prompt_details_view",
                    "title": {"type": "plain_text", "text": prompt.title, "emoji": True},
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Category:* {prompt.category}"
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": prompt.content
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {"type": "plain_text", "text": "Use", "emoji": True},
                                    "style": "primary",
                                    "action_id": f"use_prompt:{prompt.id}"
                                },
                                {
                                    "type": "button",
                                    "text": {"type": "plain_text", "text": f"{'★ Unfavorite' if is_favorite else '☆ Favorite'}", "emoji": True},
                                    "action_id": f"toggle_favorite:{prompt.id}"
                                },
                                {
                                    "type": "button",
                                    "text": {"type": "plain_text", "text": "✏️ Edit", "emoji": True},
                                    "action_id": f"edit_prompt:{prompt.id}"
                                },
                                {
                                    "type": "button",
                                    "text": {"type": "plain_text", "text": "🗑️ Delete", "emoji": True},
                                    "style": "danger",
                                    "action_id": f"delete_prompt:{prompt.id}"
                                }
                            ]
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"Created: {prompt.created_at.strftime('%Y-%m-%d')}"
                                }
                            ]
                        }
                    ],
                    "close": {"type": "plain_text", "text": "Close", "emoji": True}
                }

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

            # If not in a modal, send a confirmation message
            if not is_from_modal:
                client.chat_postEphemeral(
                    channel=user_id,
                    user=user_id,
                    text=f"{'Added to' if is_favorite else 'Removed from'} favorites!"
                )
        else:
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text="❌ Could not update favorite status. Please try again."
            )
    except Exception:
        logger.exception("Error toggling favorite status")
