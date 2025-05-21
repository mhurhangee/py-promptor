from .context import context
from .mrkdwn import mrkdwn
from .types import Block


def context_text(text: str) -> Block:
    """Create a context block with a single text element."""
    return context([mrkdwn(text)])
