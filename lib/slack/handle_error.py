"""Utility for consistent error handling in Slack actions."""
from logging import Logger

from slack_sdk import WebClient

from .send_error_eph import send_error_eph


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

    # Show an ephemeral message
    send_error_eph(client, body, message)
