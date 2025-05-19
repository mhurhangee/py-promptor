"""
Tests for the assistant module registration.
"""

import logging
from unittest.mock import Mock, patch

from slack_bolt import App

from listeners.assistant import register
from listeners.assistant.sample_assistant import assistant

test_logger = logging.getLogger(__name__)


class TestAssistantRegistration:
    """Tests for the assistant module registration."""

    def setup_method(self):
        """Set up test fixtures."""
        self.fake_app = Mock(App)

    def test_register(self):
        """Test that the register function registers the assistant middleware with the app."""
        # Call the register function
        register(self.fake_app)

        # Verify that app.use was called with the assistant
        self.fake_app.use.assert_called_once_with(assistant)

    @patch("listeners.assistant.assistant")
    def test_assistant_instance(self, mock_assistant):
        """Test that the assistant instance is properly created."""
        # Verify that the assistant instance exists
        assert assistant is not None

        # Verify that it's an instance of Assistant (indirectly through the mock)
        from slack_bolt import Assistant

        assert isinstance(assistant, Assistant)
