from typing import Any, Dict

from .plain_text import plain_text


def select_option(text: str, value: str) -> Dict[str, Any]:
    """Create an option for select menus."""
    return {
        "text": plain_text(text),
        "value": value,
    }
