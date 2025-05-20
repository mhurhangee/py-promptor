"""Handler for using a prompt from the library."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt


def use_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the use prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the prompt ID from the action_id
        action_id = body["actions"][0]["action_id"]
        prompt_id = int(action_id.split(":")[-1])

        # Get the user ID
        user_id = body["user"]["id"]

        # Get the prompt from the database
        db = next(get_db())
        prompt = Prompt.get_by_id(db, prompt_id)

        if not prompt:
            client.chat_postEphemeral(
                channel=user_id,
                user=user_id,
                text="❌ Sorry, that prompt could not be found.",
            )
            return

        # Check if this action was triggered from within a modal
        is_from_modal = body.get("container", {}).get("type") == "view"

        # If from a modal, get the view ID to properly update it
        view_id = body.get("container", {}).get("view_id") if is_from_modal else None
        # Create the modal view
        view = {
            "type": "modal",
            "callback_id": "use_prompt_view",
            "title": {"type": "plain_text", "text": prompt.title},
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
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "💡 *Tip:* Copy this prompt and paste it in your conversation with Promptor."
                        }
                    ]
                }
            ],
            "close": {"type": "plain_text", "text": "Close"}
        }

        # If triggered from the detail view modal, update that view
        if is_from_modal and view_id:
            try:
                client.views_update(
                    view_id=view_id,
                    view=view
                )
            except Exception as e:
                logger.warning("Could not update view, falling back to views_open: %s", e)
                client.views_open(
                    trigger_id=body["trigger_id"],
                    view=view
                )
        else:
            # Otherwise, open a new modal
            client.views_open(
                trigger_id=body["trigger_id"],
                view=view
            )
    except Exception:
        logger.exception("Error handling use prompt button")
