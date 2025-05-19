"""
Assistant listeners for Slack Bolt app.
This module contains listeners for assistant-related events in Slack.
"""

from slack_bolt import App

# Import handlers to ensure decorators are registered
# This must be done before registering the assistant middleware

from . import start_assistant_thread  # noqa: F401 # Has @assistant.thread_started decorator
from . import user_message  # noqa: F401 # Has @assistant.user_message decorator

# Import the assistant instance
from .sample_assistant import assistant


def register(app: App):
    """
    Register all assistant-related listeners with the Bolt app.

    Args:
        app: The Slack Bolt app instance
    """
    # Register the assistant middleware with the app
    # This connects the assistant instance to the app
    app.use(assistant)
