from typing import Optional

from .plain_text import plain_text
from .types import Element


def button(
    text: str,
    action_id: str,
    style: Optional[str] = None,
    value: Optional[str] = None,
    url: Optional[str] = None,
) -> Element:
    """
    Create a button element.

    Args:
        text: Button text
        action_id: Action identifier
        style: Optional button style ("primary", "danger", or None for default)
        value: Optional value to include with the action
        url: Optional URL for link buttons
    """
    button_element = {
        "type": "button",
        "text": plain_text(text),
        "action_id": action_id,
    }

    if style:
        button_element["style"] = style

    if value:
        button_element["value"] = value

    if url:
        button_element["url"] = url

    return button_element
