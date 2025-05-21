from .types import Text


def mrkdwn(text: str) -> Text:
    """Create a markdown text object."""
    return {"type": "mrkdwn", "text": text}
