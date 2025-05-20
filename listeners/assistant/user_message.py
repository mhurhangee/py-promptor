"""
User message handler for the Assistant feature.
This module contains the handler for user messages in assistant threads.
"""

import logging
from random import choice as random_choice

from slack_bolt import BoltContext, Say, SetStatus

from config.settings import MESSAGES, THINKING_MESSAGES
from lib.agent.agent import create_agent
from lib.utils.mrkdown import markdown_to_mrkdwn

from .assistant import assistant


@assistant.user_message
def respond_in_assistant_thread(
    payload: dict,
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    say: Say,
) -> None:
    """
    Respond to user messages in assistant threads.

    This function is called when a user sends a message in an assistant thread.
    It retrieves conversation history, processes the message, and sends a response.

    Args:
        payload: Dictionary containing the message payload
        logger: Logger instance
        context: Bolt context
        set_status: Function to set assistant status
        say: Function to send messages
    """
    try:
        # Set the assistant status to "thinking"
        set_status(random_choice(THINKING_MESSAGES))

        user_message = payload["text"]

        logger.info("User message: %s", user_message)

        # Check if required context is available
        if context.thread_ts is None:
            logger.exception("Missing thread_ts in context")
            say(MESSAGES["error_missing_context"])
            return

        # Process the user message directly with Agno's session storage
        # The thread_ts is used as the session ID to maintain conversation history

        # Run the agent with the user message
        response = create_agent(session_id=f"thread_ts_{context.thread_ts}").run(user_message)

        # Convert markdown response to Slack mrkdwn format
        slack_response = markdown_to_mrkdwn(response.content or "", logger)

        # Send the formatted response
        say(slack_response)

    except Exception as e:
        error_msg = f"Error processing assistant message: {e}"
        logger.exception(error_msg)
        say(MESSAGES["error_general"])
