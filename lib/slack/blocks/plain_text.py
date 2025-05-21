from .types import Text


def plain_text(text: str, emoji: bool = True) -> Text:
    """Create a plain text object."""
    return {"type": "plain_text", "text": text, "emoji": emoji}
