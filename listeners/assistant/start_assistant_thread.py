from logging import Logger
from random import choice as random_choice
from random import choices as random_choices

from slack_bolt import Say, SetSuggestedPrompts

from config.settings import (FOLLOWUP_TITLES, INITIAL_FOLLOWUPS, MESSAGES,
                             WELCOME_MESSAGES)

from .assistant import assistant


@assistant.thread_started
def start_assistant_thread(
    say: Say,
    set_suggested_prompts: SetSuggestedPrompts,
    logger: Logger,
):
    try:
        # Send welcome message from config
        say(random_choice(WELCOME_MESSAGES))

        # Set suggested prompts from config
        # Convert Sequence to List to satisfy the type requirements
        set_suggested_prompts(
            prompts=list(random_choices(INITIAL_FOLLOWUPS, k=3)),
            title=random_choice(FOLLOWUP_TITLES),
        )
    except Exception as e:
        error_msg = "Error starting assistant thread: {error}".format(error=e)
        logger.error(error_msg)
        say(MESSAGES["error_general"])
