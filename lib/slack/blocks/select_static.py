from typing import Any, Dict, List, Optional

from .plain_text import plain_text
from .types import Element


def select_static(
    action_id: str,
    options: List[Dict[str, Any]],
    placeholder: str = "Select an option",
    initial_option: Optional[Dict[str, Any]] = None,
) -> Element:
    """Create a static select menu element."""
    element = {
        "type": "static_select",
        "action_id": action_id,
        "placeholder": plain_text(placeholder),
        "options": options,
    }

    if initial_option:
        element["initial_option"] = initial_option

    return element
