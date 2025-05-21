from slack_bolt import App

from .add_prompt import add_prompt_shortcut_callback
from .save_message_as_prompt import save_message_as_prompt_callback
from .view_prompt_library import view_prompt_library_callback


def register(app: App) -> None:
    app.shortcut("add_prompt_shortcut")(add_prompt_shortcut_callback)
    app.shortcut("save_message_as_prompt")(save_message_as_prompt_callback)
    app.shortcut("view_prompt_library")(view_prompt_library_callback)
