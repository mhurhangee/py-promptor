import re

from slack_bolt import App

from .add_prompt_button import add_prompt_button_callback
from .delete_prompt import delete_prompt_callback
from .edit_prompt import edit_prompt_callback
from .filter_category import filter_category_callback
from .toggle_favorite import toggle_favorite_callback
from .use_prompt import use_prompt_callback
from .view_prompt_details import view_prompt_details_callback


def register(app: App) -> None:
    app.action("add_prompt_button")(add_prompt_button_callback)
    app.action("filter_category")(filter_category_callback)
    app.action(re.compile(r"use_prompt:\d+"))(use_prompt_callback)
    app.action(re.compile(r"edit_prompt:\d+"))(edit_prompt_callback)
    app.action(re.compile(r"delete_prompt:\d+"))(delete_prompt_callback)
    app.action(re.compile(r"view_prompt_details:\d+"))(view_prompt_details_callback)
    app.action(re.compile(r"toggle_favorite:\d+"))(toggle_favorite_callback)
