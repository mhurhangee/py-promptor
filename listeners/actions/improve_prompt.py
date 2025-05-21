"""Handler for the improve prompt button."""
import json
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.agent import create_improve_prompt_agent
from lib.slack import handle_error
from lib.ui import add_prompt_modal


def improve_prompt_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the improve prompt button click."""
    try:
        # Acknowledge the button click
        ack()

        # Extract the view state and ID
        view = body["view"]
        view_id = view["id"]

        # Extract the prompt content from the form
        values = view["state"]["values"]
        content = values["content_block"]["content_input"]["value"]

        # Get existing values to preserve them
        existing_title = values["title_block"]["title_input"].get("value", "")
        existing_tags = values["tags_block"]["tags_input"].get("value", "")

        # Get the selected category if any
        existing_category = None
        category_input = values["category_block"]["category_input"]
        if category_input and "selected_option" in category_input and category_input["selected_option"]:
            existing_category = category_input["selected_option"]["value"]

        # If content is empty, we can't improve the prompt
        if not content.strip():
            # Update the view with an error message
            client.views_update(
                view_id=view_id,
                view=add_prompt_modal(
                    initial_content=content,
                    initial_title=existing_title,
                    initial_category=existing_category,
                    initial_tags=existing_tags,
                    private_metadata=json.dumps({
                        "error": "Please enter some content before improving the prompt."
                    })
                )
            )
            return

        # Create the improve prompt agent
        agent = create_improve_prompt_agent()

        # Generate the improved prompt
        logger.info("Generating improved prompt for content: %s", content[:100])
        response = agent.run(content)

        # Extract the improved prompt and reasoning
        improved_prompt = getattr(response.content, "improved_prompt", "")
        reasoning = getattr(response.content, "reasoning", "")

        logger.info("Generated improved prompt: %s", improved_prompt[:100])
        logger.info("Reasoning: %s", reasoning[:100])

        # Create a display of the improved prompt and reasoning
        improved_display = f"```\n{improved_prompt}\n```\n\n*Why?*\n> {reasoning}"

        # Update the view with the original content but show improved version below
        client.views_update(
            view_id=view_id,
            view=add_prompt_modal(
                initial_content=content,  # Keep original content in the input field
                initial_title=existing_title,
                initial_category=existing_category,
                initial_tags=existing_tags,
                improved_prompt_display=improved_display,  # Pass the display to the modal
                private_metadata=json.dumps({
                    "improved": True,
                    "original_content": content,
                    "improved_content": improved_prompt,
                    "reasoning": reasoning,
                    "original_title": existing_title,
                    "original_category": existing_category,
                    "original_tags": existing_tags
                })
            )
        )

        # Send an ephemeral message with the reasoning
        client.chat_postEphemeral(
            channel=body["user"]["id"],
            user=body["user"]["id"],
            text=f"*Prompt Improvement Reasoning:*\n\n{reasoning}"
        )

    except Exception as e:
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=e,
            message="Sorry, something went wrong while improving the prompt."
        )
