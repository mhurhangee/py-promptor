"""Assistant instance for Slack Bolt app.

This module creates and exports the Assistant instance that will be used
by the event handlers to process assistant-related events.
"""

from slack_bolt import Assistant

# Create the Assistant instance with default settings
# This will handle assistant_thread_started, assistant_thread_context_changed, and message events
assistant = Assistant()
