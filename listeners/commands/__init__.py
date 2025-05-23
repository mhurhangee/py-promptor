from slack_bolt import App

from .sample_command import sample_command_callback


def register(app: App) -> None:
    app.command("/sample-command")(sample_command_callback)
