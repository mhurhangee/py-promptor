from typing import List

from .types import Block, Element


def actions(elements: List[Element]) -> Block:
    """Create an actions block."""
    return {"type": "actions", "elements": elements}
