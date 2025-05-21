from typing import Any, Dict, Optional

from lib.slack.blocks import (
    actions,
    button,
    context_text,
    input_block,
    modal,
    text_input,
)
from lib.ui.category_select import category_select


def add_prompt_modal(
    initial_content: str = "",
    initial_title: Optional[str] = None,
    initial_category: Optional[str] = None,
    initial_tags: Optional[str] = None,
    private_metadata: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a modal view for adding a new prompt.

    Args:
        initial_content: Optional initial content for the prompt
        initial_title: Optional initial title for the prompt
        initial_category: Optional initial category for the prompt
        initial_tags: Optional initial tags for the prompt (comma-separated)
        private_metadata: Optional metadata to store with the modal
    """
    blocks = [
        input_block(
            label="Title",
            block_id="title_block",
            element=text_input(
                action_id="title_input",
                placeholder="Enter a title",
                initial_value=initial_title or "",
            ),
            optional=True,
        ),
        input_block(
            label="Category",
            block_id="category_block",
            element=category_select(
                action_id="category_input",
                initial_category=initial_category,
            ),
            optional=True,
        ),
        input_block(
            label="Tags",
            block_id="tags_block",
            element=text_input(
                action_id="tags_input",
                placeholder="Enter comma-separated tags",
                initial_value=initial_tags or "",
            ),
            optional=True,
        ),
        input_block(
            label="Content",
            block_id="content_block",
            element=text_input(
                action_id="content_input",
                placeholder="Enter the prompt content",
                multiline=True,
                initial_value=initial_content,
            ),
        ),
        actions([
            button(
                text="✨ Suggest Metadata",
                action_id="suggest_metadata_button",
                style="primary",
            )
        ]),
        context_text("*Tip:* Use markdown formatting in your prompt for better readability."),
    ]

    return modal(
        title="Add Prompt",
        blocks=blocks,
        callback_id="add_prompt_modal",
        submit_text="💾",
        private_metadata=private_metadata or "",
    )
