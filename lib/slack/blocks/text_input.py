from .plain_text import plain_text
from .types import Element


def text_input(
    action_id: str,
    placeholder: str = "",
    initial_value: str = "",
    multiline: bool = False,
) -> Element:
    """Create a plain text input element."""
    element = {
        "type": "plain_text_input",
        "action_id": action_id,
        "placeholder": plain_text(placeholder),
    }

    if initial_value:
        element["initial_value"] = initial_value

    if multiline:
        element["multiline"] = True

    return element
