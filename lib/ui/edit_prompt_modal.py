from typing import Any, Dict

from lib.slack.blocks import input_block, modal, text_input
from lib.ui.category_select import category_select


def edit_prompt_modal(prompt: Any) -> Dict[str, Any]:
    """
    Create a modal view for editing a prompt.

    Args:
        prompt: A Prompt object with attributes id, title, category, content
    """
    blocks = [
        input_block(
            label="Title",
            block_id="title_block",
            element=text_input(
                action_id="title_input",
                placeholder="Enter a title",
                initial_value=prompt.title
            ),
        ),
        input_block(
            label="Category",
            block_id="category_block",
            element=category_select(
                action_id="category_input",
                initial_category=str(prompt.category),
            ),
        ),
        input_block(
            label="Content",
            block_id="content_block",
            element=text_input(
                action_id="content_input",
                placeholder="Enter the prompt content",
                initial_value=prompt.content,
                multiline=True
            ),
        ),
    ]

    return modal(
        title="Edit Prompt",
        blocks=blocks,
        callback_id="edit_prompt_view",
        submit_text="Save Changes",
        private_metadata=str(prompt.id),
    )
