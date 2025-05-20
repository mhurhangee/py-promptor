from slack_bolt import App

from .add_prompt import add_prompt_shortcut_callback
from .sample_shortcut import sample_shortcut_callback
from .view_prompt_library import view_prompt_library_callback


def register(app: App) -> None:
    app.shortcut("sample_shortcut_id")(sample_shortcut_callback)
    app.shortcut("add_prompt_shortcut")(add_prompt_shortcut_callback)
    app.shortcut("view_prompt_library_shortcut")(view_prompt_library_callback)
