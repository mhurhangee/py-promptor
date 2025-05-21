"""Handler for using a prompt from the library."""

import uuid
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.agent.agent import create_agent
from lib.db.database import get_db
from lib.db.models import Prompt
from lib.slack import get_prompt_id, get_user_id, get_view_id, handle_error, markdown_to_mrkdwn, send_error_eph
from lib.ui import loading_modal, prompt_result_modal


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
            send_error_eph(client, body, "Sorry, that prompt could not be found.")
            return

        # Get the view ID to properly update it if from a modal
        view_id = get_view_id(body)

        try:
            # Generate a unique session ID for this interaction
            session_id = f"prompt_{prompt.id}_{user_id}_{uuid.uuid4().hex[:8]}"

            # Show a loading message first
            loading_view = loading_modal(
                title="Processing Prompt",
                message=f"Processing '{prompt.title}'..."
            )

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

                # Create a modal with the AI response using the modal builder
                result_view = prompt_result_modal(
                    prompt_title=str(prompt.title),
                    prompt_content=str(prompt.content),
                    response_title=response_title,
                    response_content=slack_response
                )

                client.views_update(view_id=view_id, view=result_view)

                logger.info("Successfully processed prompt and showed AI response")

            except Exception as e:
                handle_error(
                    client=client,
                    body=body,
                    logger=logger,
                    error=e,
                    message="Failed to process the prompt with AI. Please try again."
                )

        except Exception as e:
            handle_error(
                client=client,
                body=body,
                logger=logger,
                error=e,
                message="Could not send the prompt. Please try again."
            )

    except Exception as e:
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=e,
            message="Error handling use prompt button"
        )
