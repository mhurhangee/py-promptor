from typing import Optional

from .mrkdwn import mrkdwn
from .types import Block, Element


def section(text: str, accessory: Optional[Element] = None) -> Block:
    """Create a section block with markdown text."""
    block = {"type": "section", "text": mrkdwn(text)}
    if accessory:
        block["accessory"] = accessory
    return block
