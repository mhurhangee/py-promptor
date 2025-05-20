"""Handler for the Add New Prompt button action."""
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.slack import error_eph


def add_prompt_button_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the add prompt button click."""

    try:
        # Acknowledge the button click
        ack()

        # Create the modal view
        view = {
            "type": "modal",
            "callback_id": "add_prompt_view",
            "title": {"type": "plain_text", "text": "🏛️ Add New Prompt"},
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
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter your prompt content here...",
                        },
                    },
                },
            ],
            "close": {"type": "plain_text", "text": "❌", "emoji": True},
            "submit": {"type": "plain_text", "text": "💾", "emoji": True},
        }

        client.views_open(
            trigger_id=body["trigger_id"],
            view=view
        )
    except Exception:
        logger.exception("Error handling add prompt button")
        error_eph(client, body, "Sorry, something went wrong while adding the prompt.")
