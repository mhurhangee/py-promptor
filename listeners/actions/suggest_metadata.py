"""Handler for the suggest metadata button in the add prompt modal."""
import json
import uuid
from logging import Logger

from slack_bolt import Ack
from slack_sdk import WebClient

from lib.agent import create_metadata_agent
from lib.slack import handle_error
from lib.ui import add_prompt_modal


def suggest_metadata_callback(body: dict, ack: Ack, client: WebClient, logger: Logger) -> None:
    """Handle the suggest metadata button click."""
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

        # If content is empty, we can't generate metadata
        if not content.strip():
            # Update the view with an error message
            client.views_update(
                view_id=view_id,
                view=add_prompt_modal(
                    initial_content=content,
                    initial_title=existing_title,
                    initial_category=existing_category,
                    initial_tags=existing_tags,
                    private_metadata=json.dumps({"error": "Content is required to generate metadata"})
                )
            )
            return

        # Generate a unique session ID for this interaction
        session_id = f"metadata_{uuid.uuid4().hex[:8]}"

        # Call the metadata agent to generate suggestions
        agent = create_metadata_agent(session_id=session_id)
        response = agent.run(content)

        # Extract the metadata from the response
        title = getattr(response.content, "title", "")
        category = getattr(response.content, "category", "")
        tags = getattr(response.content, "tags", "")

        # Only use AI suggestions for fields that are empty
        suggested_title = existing_title if existing_title else title
        suggested_category = existing_category if existing_category else category
        suggested_tags = existing_tags if existing_tags else tags

        # Update the modal with the suggested metadata
        client.views_update(
            view_id=view_id,
            view=add_prompt_modal(
                initial_content=content,
                initial_title=suggested_title,
                initial_category=suggested_category,
                initial_tags=suggested_tags,
                private_metadata=json.dumps({
                    "suggested": True,
                    "suggested_title": suggested_title,
                    "suggested_category": suggested_category,
                    "suggested_tags": suggested_tags,
                    "original_title": existing_title,
                    "original_category": existing_category,
                    "original_tags": existing_tags
                })
            )
        )
    except Exception as e:
        handle_error(
            client=client,
            body=body,
            logger=logger,
            error=e,
            message="Sorry, something went wrong while generating metadata suggestions."
        )
