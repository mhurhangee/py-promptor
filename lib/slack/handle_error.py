"""Utility for consistent error handling in Slack actions."""
from logging import Logger

from slack_sdk import WebClient

from .get_view_id import get_view_id
from .send_error_eph import send_error_eph
from .show_error_modal import show_error_modal


def handle_error(
    client: WebClient,
    body: dict,
    logger: Logger,
    error: Exception,
    message: str,
) -> None:
    """
    Handle errors consistently across all Slack actions.

    Args:
        client: Slack WebClient
        body: Request body
        logger: Logger instance
        error: The exception that was raised
        message: User-friendly error message
    """
    # Log the error with context
    logger.exception("Error handling action: %s", str(error))

    # Get the view ID to determine how to show the error
    view_id = get_view_id(body)

    # If we have a view ID, show the error in a modal
    # Otherwise, show an ephemeral message
    if view_id:
        show_error_modal(client, body, message)
    else:
        send_error_eph(client, body, message)
