"""UI components for the prompt library."""
from typing import List, Optional

from lib.db.database import get_db
from lib.db.models import Prompt

# Constants
PREVIEW_LENGTH = 100


def get_prompt_library_blocks(user_id: str, show_add_button: bool = True, filtered_prompts: Optional[List[Prompt]] = None) -> List[dict]:
    """
    Generate blocks for displaying the prompt library.

    Args:
        user_id: The ID of the user whose prompts to display
        show_add_button: Whether to show the "Add New Prompt" button

    Returns:
        A list of block elements for displaying in a home tab
    """
    # Get the user's prompts from the database or use filtered prompts if provided
    if filtered_prompts is None:
        db = next(get_db())
        prompts = Prompt.get_all_by_user(db, user_id)
    else:
        prompts = filtered_prompts

    # Create the header blocks
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "Your Prompt Library", "emoji": True},
        }
    ]

    # Add a search box for filtering prompts (to be implemented later)
    blocks.append(
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Search and filter your prompts:*"
            },
        }
    )

    # This is a placeholder for future search functionality
    blocks.append(
        {
            "type": "actions",
            "elements": [
                {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Filter by category",
                        "emoji": True
                    },
                    "options": [
                        {
                            "text": {"type": "plain_text", "text": "All Prompts", "emoji": True},
                            "value": "all"
                        },
                        {
                            "text": {"type": "plain_text", "text": "★ Favorites Only", "emoji": True},
                            "value": "favorites"
                        },
                        {
                            "text": {"type": "plain_text", "text": "General", "emoji": True},
                            "value": "General"
                        },
                        {
                            "text": {"type": "plain_text", "text": "Writing", "emoji": True},
                            "value": "Writing"
                        },
                        {
                            "text": {"type": "plain_text", "text": "Coding", "emoji": True},
                            "value": "Coding"
                        },
                        {
                            "text": {"type": "plain_text", "text": "Marketing", "emoji": True},
                            "value": "Marketing"
                        },
                        {
                            "text": {"type": "plain_text", "text": "Other", "emoji": True},
                            "value": "Other"
                        }
                    ],
                    "action_id": "filter_category"
                }
            ]
        }
    )

    # Add a divider before the prompts
    blocks.append({"type": "divider"})

    # Add the Add New Prompt button at the top if requested
    if show_add_button:
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Add New Prompt", "emoji": True},
                        "style": "primary",
                        "action_id": "add_prompt_button",
                    }
                ],
            }
        )
    blocks.append({"type": "divider"})

    # Add prompts to the view if they exist
    if prompts:
        # Group prompts by category
        prompts_by_category = {}
        for prompt in prompts:
            category = prompt.category or "Uncategorized"
            if category not in prompts_by_category:
                prompts_by_category[category] = []
            prompts_by_category[category].append(prompt)

        # Add each category and its prompts
        for category, category_prompts in prompts_by_category.items():
            # Add category header
            blocks.append(
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": category, "emoji": True},
                }
            )

            # Add each prompt in this category with a simplified view
            for prompt in category_prompts:
                # Add the prompt title and a snippet of the content with a View button
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{prompt.title}* {':star:' if bool(prompt.is_favorite) else ''}\n{prompt.content[:PREVIEW_LENGTH]}{'...' if len(prompt.content) > PREVIEW_LENGTH else ''}",
                        },
                        "accessory": {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "View", "emoji": True},
                            "action_id": f"view_prompt_details:{prompt.id}",
                        },
                    }
                )

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
