import re

from slack_bolt import App

from .add_prompt_button import add_prompt_button_callback
from .delete_prompt import delete_prompt_callback
from .sample_action import sample_action_callback
from .use_prompt import use_prompt_callback
from .view_prompts_modal import view_prompts_modal_callback


def register(app: App) -> None:
    app.action("sample_action_id")(sample_action_callback)
    app.action("add_prompt_button")(add_prompt_button_callback)
    app.action("view_prompts_modal")(view_prompts_modal_callback)
    app.action(re.compile(r"use_prompt:\d+"))(use_prompt_callback)
    app.action(re.compile(r"delete_prompt:\d+"))(delete_prompt_callback)
