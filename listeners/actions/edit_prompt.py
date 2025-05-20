"""Handler for editing a prompt from the library."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt


def edit_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the edit prompt button click."""
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
            "callback_id": "edit_prompt_view",
            "private_metadata": str(prompt.id),  # Store the prompt ID in private_metadata
            "title": {"type": "plain_text", "text": "Edit Prompt", "emoji": True},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "prompt_title_block",
                    "label": {
                        "type": "plain_text",
                        "text": "Prompt Title",
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "prompt_title_input",
                        "initial_value": prompt.title,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter a descriptive title for your prompt",
                        },
                    },
                },
                {
                    "type": "input",
                    "block_id": "prompt_category_block",
                    "label": {
                        "type": "plain_text",
                        "text": "Category",
                    },
                    "element": {
                        "type": "static_select",
                        "action_id": "prompt_category_select",
                        "initial_option": {
                            "text": {"type": "plain_text", "text": prompt.category},
                            "value": prompt.category,
                        },
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a category",
                        },
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "General"},
                                "value": "General",
                            },
                            {
                                "text": {"type": "plain_text", "text": "Writing"},
                                "value": "Writing",
                            },
                            {
                                "text": {"type": "plain_text", "text": "Coding"},
                                "value": "Coding",
                            },
                            {
                                "text": {"type": "plain_text", "text": "Marketing"},
                                "value": "Marketing",
                            },
                            {
                                "text": {"type": "plain_text", "text": "Other"},
                                "value": "Other",
                            },
                        ],
                    },
                },
                {
                    "type": "input",
                    "block_id": "prompt_content_block",
                    "label": {
                        "type": "plain_text",
                        "text": "Prompt Content",
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "prompt_content_input",
                        "multiline": True,
                        "initial_value": prompt.content,
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter your prompt content here...",
                        },
                    },
                },
            ],
            "submit": {"type": "plain_text", "text": "Save Changes", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
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
        logger.exception("Error handling edit prompt button")
