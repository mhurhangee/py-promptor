from slack_bolt import App

from .add_prompt_view import add_prompt_view_callback
from .delete_prompt_confirmation import delete_prompt_confirmation_callback
from .edit_prompt_view import edit_prompt_view_callback
from .sample_view import sample_view_callback


def register(app: App) -> None:
    app.view("sample_view_id")(sample_view_callback)
    app.view("add_prompt_view")(add_prompt_view_callback)
    app.view("edit_prompt_view")(edit_prompt_view_callback)
    app.view("delete_prompt_confirmation")(delete_prompt_confirmation_callback)
