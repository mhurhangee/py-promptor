"""UI component for category selection."""
from typing import Any, Dict, List, Optional

from config.categories import DEFAULT_CATEGORIES
from lib.slack.blocks import select_option, select_static


def category_select(
    action_id: str,
    placeholder: str = "Select a category",
    initial_category: Optional[str] = None,
    categories: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """
    Create a category select dropdown element.

    Args:
        action_id: The action ID for the select element
        placeholder: Placeholder text to display
        initial_category: The initially selected category (if any)
        categories: Optional custom categories list. If not provided, DEFAULT_CATEGORIES is used.

    Returns:
        A select_static element configured with the appropriate categories
    """
    # Use provided categories or default ones
    category_options = categories or DEFAULT_CATEGORIES

    # Create select options from categories
    options = [
        select_option(category["text"], category["value"])
        for category in category_options
    ]

    # If initial category is provided, create initial_option
    initial_option = None
    if initial_category:
        matching_categories = [c for c in category_options if c["value"] == initial_category]
        if matching_categories:
            category = matching_categories[0]
            initial_option = select_option(category["text"], category["value"])

    return select_static(
        action_id=action_id,
        placeholder=placeholder,
        options=options,
        initial_option=initial_option,
    )
