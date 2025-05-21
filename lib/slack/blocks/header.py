
from .plain_text import plain_text
from .types import Block


def header(text: str) -> Block:
    """Create a header block."""
    return {"type": "header", "text": plain_text(text)}
