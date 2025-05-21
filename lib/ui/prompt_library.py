"""UI components for the prompt library."""
from typing import Dict, List, Optional

from config.categories import ALL_CATEGORIES_VALUE, DEFAULT_CATEGORIES
from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack.blocks import (
    actions,
    button,
    divider,
    header,
    section,
    select_option,
    select_static,
)
from lib.ui.prompt_metadata import create_prompt_context_block

# Constants
PREVIEW_LENGTH = 100


def get_prompt_library_blocks(user_id: str, filtered_prompts: Optional[List[Prompt]] = None) -> List[dict]:
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
        header(":books: Your Prompt Library"),
        # Category filter dropdown
        actions([
            _create_category_filter_dropdown(),
            button(
                text="Add New Prompt",
                action_id="add_prompt_button",
                style="primary"
            )
        ]),
        # Add a divider before the prompts
        divider(),
    ]

    # Add prompts to the view if they exist
    if prompts:
        # Add each prompt to the blocks
        for prompt in prompts:
            # Add the favorite star if applicable
            title_prefix = "⭐ " if bool(prompt.is_favorite) else ""

            # Add the prompt block with View button - just show the title, no content
            blocks.append(
                section(
                    f"*{title_prefix}{prompt.title}*",
                    accessory=button(
                        text="View",
                        action_id=f"view_prompt_details:{prompt.id}"
                    )
                )
            )
            # Add a context block with the category
            blocks.append(
                create_prompt_context_block(prompt)
            )
            blocks.append(divider())

    else:
        # If there are no prompts, show a message
        blocks.append(
            section("*You don't have any prompts yet.* Click the button above to add your first prompt! Or select a message in a conversation.")
        )
    return blocks


def _create_category_filter_dropdown() -> Dict:
    """Create a dropdown for filtering prompts by category."""
    # Start with special options
    options = [
        select_option("🦕 All prompts", ALL_CATEGORIES_VALUE),
        select_option("⭐ Favorites only", "favorites"),
    ]

    # Add category options from the centralized config
    for category in DEFAULT_CATEGORIES:
        options.append(select_option(category["text"], category["value"]))
    return select_static(
        action_id="filter_category",
        placeholder="Filter by category",
        options=options
    )



