import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Initialization
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    # Set to True to ignore self-messages and prevent loops
    # Only set to False if you need to process your own bot messages
    ignoring_self_assistant_message_events_enabled=True,
)

# Register listeners
register_listeners(app)

# Start Bolt app
if __name__ == "__main__":
    logger.info("Starting Promptor Slack app...")
    try:
        SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
    except Exception as e:
        logger.error(f"Error starting app: {e}")

