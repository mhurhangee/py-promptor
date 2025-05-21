from typing import Any, Dict

from lib.slack.blocks import context_text, input_block, modal, text_input
from lib.ui.category_select import category_select


def add_prompt_modal(initial_content: str = "") -> Dict[str, Any]:
    """Create a modal view for adding a new prompt.

    Args:
        initial_content: Optional initial content for the prompt
    """
    blocks = [
        input_block(
            label="Title",
            block_id="title_block",
            element=text_input(
                action_id="title_input",
                placeholder="Enter a title"
            ),
        ),
        input_block(
            label="Category",
            block_id="category_block",
            element=category_select(action_id="category_input"),
        ),
        input_block(
            label="Content",
            block_id="content_block",
            element=text_input(
                action_id="content_input",
                placeholder="Enter the prompt content",
                multiline=True,
                initial_value=initial_content
            ),
        ),
        context_text("*Tip:* Use markdown formatting in your prompt for better readability."),
    ]

    return modal(
        title="Add Prompt",
        blocks=blocks,
        callback_id="add_prompt_modal",
        submit_text="💾",
    )
