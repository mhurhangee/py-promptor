from typing import Any, Dict, List, Optional

from .plain_text import plain_text
from .types import Block


def modal(  # noqa: PLR0913
    title: str,
    blocks: List[Block],
    callback_id: str,
    submit_text: Optional[str] = None,
    close_text: str = "Close",
    private_metadata: str = "",
    clear_on_close: bool = False,
    notify_on_close: bool = False,
) -> Dict[str, Any]:
    """
    Create a modal view.

    Args:
        title: Modal title
        blocks: List of blocks to include in the modal
        callback_id: Callback identifier for the modal
        submit_text: Text for the submit button (if None, no submit button is shown)
        close_text: Text for the close button
        private_metadata: Optional metadata to include with the modal
        clear_on_close: Whether to clear the modal when closed
        notify_on_close: Whether to send a notification when the modal is closed
    """
    view = {
        "type": "modal",
        "callback_id": callback_id,
        "title": plain_text(title),
        "blocks": blocks,
        "close": plain_text(close_text),
    }

    if submit_text:
        view["submit"] = plain_text(submit_text)

    if private_metadata:
        view["private_metadata"] = private_metadata

    if clear_on_close:
        view["clear_on_close"] = True

    if notify_on_close:
        view["notify_on_close"] = True

    return view
