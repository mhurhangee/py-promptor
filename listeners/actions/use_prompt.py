"""Handler for using a prompt from the library."""

import uuid
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.agent.agent import create_agent
from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import error_eph, error_modal, get_prompt_id, get_user_id, get_view_id, markdown_to_mrkdwn


def use_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the use prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the prompt ID from the action_id
        prompt_id = get_prompt_id(body)

        # Get the user ID
        user_id = get_user_id(body)

        # Get the prompt from the database
        db = next(get_db())
        prompt = Prompt.get_by_id(db, prompt_id)

        if not prompt:
            error_eph(client, body, "Sorry, that prompt could not be found.")
            return

        # Get the view ID to properly update it if from a modal
        view_id = get_view_id(body)

        try:
            # Generate a unique session ID for this interaction
            session_id = f"prompt_{prompt.id}_{user_id}_{uuid.uuid4().hex[:8]}"

            # Show a loading message first
            loading_view = {
                "type": "modal",
                "callback_id": "prompt_loading",
                "title": {"type": "plain_text", "text": "Processing Prompt"},
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f":hourglass_flowing_sand: Processing prompt *{prompt.title}*... Please wait.",
                        },
                    }
                ],
                "close": {"type": "plain_text", "text": "Cancel"},
            }

            client.views_update(view_id=view_id, view=loading_view)

            try:
                # Send the prompt to the AI agent
                agent = create_agent(session_id=session_id)
                # Convert prompt.content to string to ensure it's the right type
                prompt_text = str(prompt.content)
                response = agent.run(prompt_text)

                # Get the content object safely
                content = getattr(response, "content", None)

                # Get the response text safely
                ai_response = getattr(content, "response", "") if content else ""
                response_title = getattr(content, "response_title", "") if content else ""

                if not ai_response:
                    logger.warning("No response text found in the agent response")

                # Format the response for Slack
                slack_response = markdown_to_mrkdwn(ai_response, logger)

                # Create a modal with the AI response
                result_view = {
                    "type": "modal",
                    "callback_id": "prompt_result_view",
                    "title": {"type": "plain_text", "text": "AI Response"},
                    "blocks": [
                        {"type": "header", "text": {"type": "plain_text", "text": prompt.title}},
                        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Original Prompt:*\n_{prompt.content}_"}},
                        {"type": "divider"},
                        {"type": "section", "text": {"type": "mrkdwn", "text": f"*{response_title}*"}},
                        {"type": "section", "text": {"type": "mrkdwn", "text": slack_response}},
                    ],
                    "close": {"type": "plain_text", "text": "Close"},
                }

                client.views_update(view_id=view_id, view=result_view)

                logger.info("Successfully processed prompt and showed AI response")

            except Exception:
                logger.exception("Error processing prompt with AI")
                error_message ="Failed to process the prompt with AI. Please try again."
                error_modal(client, body, error_message)

        except Exception:
            # Handle errors
            logger.exception("Error sending prompt")
            error_message = "Could not send the prompt. Please try again."
            error_modal(client, body, error_message)

    except Exception:
        logger.exception("Error handling use prompt button")
