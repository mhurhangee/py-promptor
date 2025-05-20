from logging import Logger

from slack_sdk import WebClient

from lib.slack import md_section


def app_home_opened_callback(client: WebClient, event: dict, logger: Logger) -> None:
    # ignore the app_home_opened event for anything but the Home tab
    if event["tab"] != "home":
        return
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    md_section("Welcome to *Promptor*, <@" + event["user"] + "> 🦕"),
                    md_section("This is your prompt library!"),
                ],
            },
        )
    except Exception:
        logger.exception("Error publishing home tab")
