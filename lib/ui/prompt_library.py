"""UI components for the prompt library."""
from typing import List

from lib.db.database import get_db
from lib.db.models import Prompt


def get_prompt_library_blocks(user_id: str, show_add_button: bool = True, show_modal_button: bool = False) -> List[dict]:
    """
    Generate blocks for displaying the prompt library.

    Args:
        user_id: The ID of the user whose prompts to display
        show_add_button: Whether to show the "Add New Prompt" button
        show_modal_button: Whether to show the "View as Modal" button

    Returns:
        A list of block elements for displaying in a home tab or modal
    """
    # Get the user's prompts from the database
    db = next(get_db())
    prompts = Prompt.get_all_by_user(db, user_id)

    # Create the header blocks
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "📚 Your Prompt Library"}
        }
    ]

    # Add action buttons if needed
    action_elements = []

    if show_add_button:
        action_elements.append({
            "type": "button",
            "text": {"type": "plain_text", "text": "+ Add New Prompt!!!", "emoji": True},
            "style": "primary",
            "action_id": "add_prompt_button"
        })

    if show_modal_button:
        action_elements.append({
            "type": "button",
            "text": {"type": "plain_text", "text": "🔍 View as Modal", "emoji": True},
            "action_id": "view_prompts_modal"
        })

    if action_elements:
        blocks.append({
            "type": "actions",
            "elements": action_elements
        })

    blocks.append({"type": "divider"})

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
                        "text": {"type": "plain_text", "text": "Use", "emoji": True},
                        "style": "primary",
                        "value": str(prompt.id),
                        "action_id": f"use_prompt:{prompt.id}"
                    }
                })

                # Add action buttons for this prompt
                blocks.append({
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "🗑️ Delete", "emoji": True},
                            "style": "danger",
                            "value": str(prompt.id),
                            "action_id": f"delete_prompt:{prompt.id}",
                            "confirm": {
                                "title": {"type": "plain_text", "text": "Delete Prompt"},
                                "text": {"type": "mrkdwn", "text": f"Are you sure you want to delete *{prompt.title}*? This cannot be undone."},
                                "confirm": {"type": "plain_text", "text": "Delete"},
                                "deny": {"type": "plain_text", "text": "Cancel"}
                            }
                        }
                    ]
                })

                # Add a divider between prompts
                blocks.append({"type": "divider"})
    else:
        # No prompts message
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You don't have any prompts yet. Click the button above to add your first prompt!"
            }
        })

    return blocks
