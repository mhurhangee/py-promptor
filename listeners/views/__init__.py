from slack_bolt import App

from .add_prompt_view import add_prompt_view_callback
from .sample_view import sample_view_callback


def register(app: App) -> None:
    app.view("sample_view_id")(sample_view_callback)
    app.view("add_prompt_view")(add_prompt_view_callback)
