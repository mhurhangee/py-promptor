from logging import Logger
from typing import Optional

from slack_sdk import WebClient

from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import md_section


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
        # Get the user's prompts from the database
        db = next(get_db())
        prompts = Prompt.get_all_by_user(db, user_id)

        # Create the home tab view
        blocks = [
            md_section("Welcome to *Promptor*, <@" + user_id + "> 🦕"),
            md_section("This is your prompt library!"),
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "+ Add New Prompt"},
                        "action_id": "add_prompt_button",
                        "style": "primary",
                    }
                ],
            },
            {"type": "divider"},
        ]

        # Add prompts to the view if they exist
        if prompts:
            # Group prompts by category
            prompts_by_category = {}
            for prompt in prompts:
                if prompt.category not in prompts_by_category:
                    prompts_by_category[prompt.category] = []
                prompts_by_category[prompt.category].append(prompt)

            # Add each category and its prompts
            for category, category_prompts in prompts_by_category.items():
                # Add category header
                blocks.append({
                    "type": "header",
                    "text": {"type": "plain_text", "text": category}
                })

                # Add each prompt in this category
                for prompt in category_prompts:
                    # Define a constant for preview length
                    preview_length = 100
                    blocks.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{prompt.title}*\n{prompt.content[:preview_length]}{'...' if len(prompt.content) > preview_length else ''}"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "Use"},
                            "value": str(prompt.id),
                            "action_id": f"use_prompt:{prompt.id}"
                        }
                    })
        else:
            # No prompts message
            blocks.append(md_section("You don't have any prompts yet. Click the button above to add your first prompt!"))

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
