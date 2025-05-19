"""
User message handler for the Assistant feature.
This module contains the handler for user messages in assistant threads.
"""

import logging
from typing import Dict, List

from slack_bolt import BoltContext, Say, SetStatus
from slack_sdk import WebClient

from .sample_assistant import assistant


@assistant.user_message
def respond_in_assistant_thread(
    payload: dict,
    logger: logging.Logger,
    context: BoltContext,
    set_status: SetStatus,
    client: WebClient,
    say: Say,
):
    """
    Respond to user messages in assistant threads.

    This function is called when a user sends a message in an assistant thread.
    It retrieves conversation history, processes the message, and sends a response.

    Args:
        payload: The event payload
        logger: Logger instance
        context: Bolt context
        set_status: Function to set assistant status
        client: Slack WebClient instance
        say: Function to send messages
    """
    try:

        # Set the assistant status to "typing"
        set_status("is typing...")

        # Collect conversation history from the thread
        # Add type checking to ensure channel_id and thread_ts are not None
        if context.channel_id is None or context.thread_ts is None:
            logger.error("Missing channel_id or thread_ts in context")
            say(":warning: Sorry, I couldn't process your request due to missing context information.")
            return

        replies = client.conversations_replies(
            channel=context.channel_id,
            ts=context.thread_ts,
            oldest=context.thread_ts,
            limit=10,
        )

        # Format messages for processing
        messages_in_thread: List[Dict[str, str]] = []
        # Check if messages exist in the response
        if "messages" not in replies or not isinstance(replies.get("messages"), list) or not replies.get("messages"):
            logger.warning("No messages found in thread")
            say(":thinking_face: I couldn't find our conversation history. Let's start fresh!")
            return

        for message in replies.get("messages", []):
            role = "user" if message.get("bot_id") is None else "assistant"
            messages_in_thread.append({"role": role, "content": message.get("text", "")})

        # TODO: Replace this with your actual LLM call
        # For now, we'll just echo back a simple response
        user_message = payload.get("text", "")
        returned_message = (
            f"I received your message: '{user_message}'\n\nThis is a placeholder response."
            + "\nYou'll need to implement the actual LLM integration."
        )

        # Send the response
        say(returned_message)

    except Exception as e:
        error_msg = f"Error processing assistant message: {e}"
        logger.error(error_msg)
        say(f":warning: Sorry, something went wrong: {e}")
