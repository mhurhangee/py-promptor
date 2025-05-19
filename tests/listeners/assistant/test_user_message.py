"""
Tests for the user_message handler.
"""

import logging
from unittest.mock import Mock, MagicMock

from slack_bolt import BoltContext, Say
from slack_sdk import WebClient

from listeners.assistant.user_message import respond_in_assistant_thread

test_logger = logging.getLogger(__name__)


class TestUserMessage:
    """Tests for the respond_in_assistant_thread handler."""

    def setup_method(self):
        """Set up test fixtures."""
        self.fake_payload = {"text": "Hello, assistant!"}
        self.fake_context = MagicMock(BoltContext)
        self.fake_context.channel_id = "C123"
        self.fake_context.thread_ts = "1621234567.123456"

        # Create a proper mock for SetStatus that accepts the required channel_id parameter
        self.fake_set_status = Mock()
        self.fake_set_status.return_value = None

        self.fake_client = Mock(WebClient)
        self.fake_say = Mock(Say)

        # Set up the conversations_replies mock to return a valid response
        self.fake_replies = {
            "messages": [
                {"bot_id": None, "text": "Hello, assistant!", "user": "U123"},
                {"bot_id": "B123", "text": "Hi there! How can I help?", "user": None},
            ]
        }
        self.fake_client.conversations_replies.return_value = self.fake_replies

    def test_respond_in_assistant_thread_success(self):
        """Test that the handler processes messages and sends a response."""
        # Call the handler
        respond_in_assistant_thread(
            payload=self.fake_payload,
            logger=test_logger,
            context=self.fake_context,
            set_status=self.fake_set_status,
            client=self.fake_client,
            say=self.fake_say,
        )

        # Verify that set_status was called
        self.fake_set_status.assert_called_once()

        # Verify that conversations_replies was called with the correct parameters
        self.fake_client.conversations_replies.assert_called_once_with(
            channel=self.fake_context.channel_id,
            ts=self.fake_context.thread_ts,
            oldest=self.fake_context.thread_ts,
            limit=10,
        )

        # Verify that say was called with a response containing the user's message
        self.fake_say.assert_called_once()
        response = self.fake_say.call_args.args[0]
        assert self.fake_payload["text"] in response

    def test_missing_context(self):
        """Test handling of missing channel_id or thread_ts in context."""
        # Set channel_id to None
        self.fake_context.channel_id = None

        # Call the handler
        respond_in_assistant_thread(
            payload=self.fake_payload,
            logger=test_logger,
            context=self.fake_context,
            set_status=self.fake_set_status,
            client=self.fake_client,
            say=self.fake_say,
        )

        # Verify that conversations_replies was not called
        self.fake_client.conversations_replies.assert_not_called()

        # Verify that say was called with an error message
        self.fake_say.assert_called_once()
        error_msg = self.fake_say.call_args.args[0]
        assert "missing context" in error_msg.lower()

    def test_no_messages_in_thread(self):
        """Test handling of no messages in the thread."""
        # Set up the conversations_replies mock to return an empty response
        self.fake_client.conversations_replies.return_value = {"messages": []}

        # Call the handler
        respond_in_assistant_thread(
            payload=self.fake_payload,
            logger=test_logger,
            context=self.fake_context,
            set_status=self.fake_set_status,
            client=self.fake_client,
            say=self.fake_say,
        )

        # Verify that say was called with an appropriate message
        self.fake_say.assert_called_once()
        msg = self.fake_say.call_args.args[0]
        assert "couldn't find" in msg.lower()

    def test_conversations_replies_exception(self, caplog):
        """Test handling of exceptions in conversations_replies."""
        # Set up the mock to raise an exception
        self.fake_client.conversations_replies.side_effect = Exception("API error")

        # Call the handler - this will raise an exception but we expect it to be caught
        # and logged in the handler
        try:
            respond_in_assistant_thread(
                payload=self.fake_payload,
                logger=test_logger,
                context=self.fake_context,
                set_status=self.fake_set_status,
                client=self.fake_client,
                say=self.fake_say,
            )
        except Exception:
            # The exception is expected to propagate in the test environment
            pass

        # Verify that the exception was logged
        assert "API error" in caplog.text

    def test_say_exception(self, caplog):
        """Test handling of exceptions in say."""
        # Set up the mock to raise an exception
        self.fake_say.side_effect = Exception("say error")

        # Call the handler - this will raise an exception but we expect it to be caught
        # and logged in the handler
        try:
            respond_in_assistant_thread(
                payload=self.fake_payload,
                logger=test_logger,
                context=self.fake_context,
                set_status=self.fake_set_status,
                client=self.fake_client,
                say=self.fake_say,
            )
        except Exception:
            # The exception is expected to propagate in the test environment
            pass

        # Verify that the exception was logged
        assert "say error" in caplog.text
