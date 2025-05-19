from logging import Logger

from slack_bolt import Say, SetSuggestedPrompts

from .assistant import assistant


@assistant.thread_started
def start_assistant_thread(
    say: Say,
    set_suggested_prompts: SetSuggestedPrompts,
    logger: Logger,
):
    try:
        say("Hello! I'm an AI assistant. How can I help you?")

        # Optionally, you could use thread_context to customize prompts per channel/thread
        set_suggested_prompts(
            prompts=[
                {
                    "title": "Ask me anything",
                    "message": "Ask me anything",
                }
            ]
        )
    except Exception as e:
        error_msg = "Error starting assistant thread: {error}".format(error=e)
        logger.error(error_msg)
        say(error_msg)
