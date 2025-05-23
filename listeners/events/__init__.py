from slack_bolt import App

from .app_home_opened import app_home_opened_callback


def register(app: App) -> None:
    # Register standard event handlers
    app.event("app_home_opened")(app_home_opened_callback)
