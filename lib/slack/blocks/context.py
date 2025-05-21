from typing import Any, Dict, List

from .types import Block


def context(elements: List[Dict[str, Any]]) -> Block:
    """Create a context block."""
    return {"type": "context", "elements": elements}
