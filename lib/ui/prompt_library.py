"""UI components for the prompt library."""
from typing import Dict, List, Optional

from config.categories import ALL_CATEGORIES_VALUE, DEFAULT_CATEGORIES
from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack.blocks import (
    actions,
    button,
    context_text,
    divider,
    header,
    section,
    select_option,
    select_static,
)

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
        header("Your Prompt Library"),
        # Add a search box for filtering prompts
        section("*Search and filter your prompts:*"),
        # Category filter dropdown
        actions([
            _create_category_filter_dropdown()
        ]),
        # Add a divider before the prompts
        divider()
    ]

    # Add the Add New Prompt button at the top if requested
    if show_add_button:
        blocks.append(
            actions([
                button(
                    text="Add New Prompt",
                    action_id="add_prompt_button",
                    style="primary"
                )
            ])
        )
    blocks.append({"type": "divider"})

    # Add prompts to the view if they exist
    if prompts:
        # Add each prompt to the blocks
        for prompt in prompts:
            # Create a preview of the prompt content
            content_preview = str(prompt.content)
            if len(content_preview) > PREVIEW_LENGTH:
                content_preview = content_preview[:PREVIEW_LENGTH] + "..."

            # Add the favorite star if applicable
            title_prefix = "★ " if bool(prompt.is_favorite) else ""
            # Add the prompt block with View button
            blocks.append(
                section(
                    f"*{title_prefix}{prompt.title}*\n{content_preview}",
                    accessory=button(
                        text="View",
                        action_id=f"view_prompt_details:{prompt.id}"
                    )
                )
            )
            # Add a context block with the category
            blocks.append(
                _create_prompt_context_block(prompt)
            )
            # Add a divider between prompts
            blocks.append(divider())
    else:
        # If there are no prompts, show a message
        blocks.append(
            section("*You don't have any prompts yet.* Click the button above to add your first prompt!")
        )
    return blocks


def _create_category_filter_dropdown() -> Dict:
    """Create a dropdown for filtering prompts by category."""
    # Start with special options
    options = [
        select_option("All Prompts", ALL_CATEGORIES_VALUE),
        select_option("★ Favorites Only", "favorites"),
    ]
    # Add category options from the centralized config
    for category in DEFAULT_CATEGORIES:
        options.append(select_option(category["text"], category["value"]))
    return select_static(
        action_id="filter_category",
        placeholder="Filter by category",
        options=options
    )


def _create_prompt_context_block(prompt: Prompt) -> Dict:
    """Create a context block with prompt metadata."""
    return context_text(
        f"Category: *{prompt.category}* | Created: {prompt.created_at.strftime('%Y-%m-%d')}"
    )
