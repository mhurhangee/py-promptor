from logging import Logger

from markdown_to_mrkdwn import SlackMarkdownConverter


def markdown_to_mrkdwn(returned_message: str, logger: Logger) -> str:
    """
    Convert Markdown to Slack mrkdwn format.

    Args:
        returned_message: Markdown string.
        logger: Logger instance for error reporting.

    Returns:
        mrkdwn-formatted string or the original message if conversion fails.
    """
    if not returned_message:
        return ""

    try:
        converter = SlackMarkdownConverter()
        return converter.convert(returned_message)
    except Exception as e:
        error_msg = f"Markdown to mrkdwn conversion failed: {e}"
        logger.exception(error_msg)
        # Return the original message as fallback
        return returned_message
