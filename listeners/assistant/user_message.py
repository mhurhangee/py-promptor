"""
User message handler for the Assistant feature.
This module contains the handler for user messages in assistant threads.
"""

import logging
from random import choice as random_choice

from slack_bolt import BoltContext, Say, SetStatus, SetSuggestedPrompts, SetTitle

from config.settings import FOLLOWUP_TITLES, MESSAGES, THINKING_MESSAGES
from lib.agent.agent import create_agent
from lib.slack import markdown_to_mrkdwn, md_section, text_context

from .assistant import assistant


@assistant.user_message
def respond_in_assistant_thread(  # noqa: PLR0913
    payload: dict,
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    set_title: SetTitle,
    set_suggested_prompts: SetSuggestedPrompts,
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

        # Check if we got a response from the agent
        if response is None:
            logger.exception("Failed to get response from agent")
            say(MESSAGES["error_general"])
            return

        # Get the content object safely
        content = getattr(response, "content", None)

        # Get the response text safely
        llm_response_text = getattr(content, "response", "") if content else ""
        thread_title = getattr(content, "thread_title", "") if content else ""
        response_title = getattr(content, "response_title", "") if content else ""
        follow_ups = getattr(content, "follow_ups", []) if content else []

        if not llm_response_text:
            logger.warning("No response text found in the agent response")
            say(MESSAGES["error_general"])
            return

        set_title(thread_title)

        # Format and send the response
        slack_response = markdown_to_mrkdwn(llm_response_text, logger)
        say(
            blocks=[
                text_context(response_title),
                md_section(slack_response),
            ]
        )

        random_follow_up = random_choice(FOLLOWUP_TITLES)

        set_suggested_prompts(follow_ups, title=random_follow_up)

    except Exception as e:
        error_msg = f"Error processing assistant message: {e}"
        logger.exception(error_msg)
        say(MESSAGES["error_general"])
