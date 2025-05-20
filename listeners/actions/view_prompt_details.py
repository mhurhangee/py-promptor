"""Handler for viewing prompt details."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import error_eph, get_prompt_id


def view_prompt_details_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the view prompt details button click."""
    try:
        # Acknowledge the button click
        ack()

        # Get prompt ID and user id
        prompt_id = get_prompt_id(body)

        # Get the prompt from the database
        db = next(get_db())
        prompt = Prompt.get_by_id(db, prompt_id)

        if not prompt:
            error_eph(client, body, "Sorry, that prompt could not be found.")
            return

        # Create the modal view with all action buttons
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
                            "text": {"type": "plain_text", "text": "★ Unfavorite" if bool(prompt.is_favorite) else "☆ Favorite", "emoji": True},
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

        # Open the modal
        client.views_open(
            trigger_id=body["trigger_id"],
            view=view
        )
    except Exception:
        logger.exception("Error handling view prompt details button")
        error_eph(client, body, "Sorry, something went wrong while viewing the prompt details.")
