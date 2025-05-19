from logging import Logger
from typing import Any

from slack_bolt import Ack, Respond


def sample_command_callback(command: Any, ack: Ack, respond: Respond, logger: Logger) -> None:
    try:
        ack()
        respond(f"Responding to the sample command! Your command was: {command['text']}")
    except Exception:
        logger.exception("Error processing sample command")
