from typing import Optional

from .plain_text import plain_text
from .types import Block, Element


def input_block(
    label: str,
    block_id: str,
    element: Element,
    optional: bool = False,
    hint: Optional[str] = None,
) -> Block:
    """Create an input block."""
    block = {
        "type": "input",
        "block_id": block_id,
        "label": plain_text(label),
        "element": element,
        "optional": optional,
    }

    if hint:
        block["hint"] = plain_text(hint)

    return block
