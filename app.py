import logging
import os

from rich.logging import RichHandler
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from lib.db.database import init_db
from listeners import register_listeners

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler()],
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
        # Initialize the database
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully")

        # Start the Socket Mode handler
        SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
    except Exception:
        logger.exception("Error starting app")
