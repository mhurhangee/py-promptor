from typing import Any, Dict

from lib.slack.blocks import modal, section

# Slack limits modal titles to 24 characters
MAX_TITLE_LENGTH = 24


def loading_modal(title: str = "Processing", message: str = "Please wait...") -> Dict[str, Any]:
    """Create a loading modal view."""
    # Ensure title is within Slack's character limit
    if len(title) > MAX_TITLE_LENGTH:
        title = title[:21] + "..."

    blocks = [section(f":hourglass_flowing_sand: {message}")]
    return modal(
        title=title,
        blocks=blocks,
        callback_id="loading_modal",
    )
