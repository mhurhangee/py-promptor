from logging import Logger

from slack_sdk import WebClient


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
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome home, <@" + event["user"] + "> :house:*",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Learn how home tabs can be more useful and "
                            "interactive <https://api.slack.com/surfaces/tabs/using|*in the documentation*>.",
                        },
                    },
                ],
            },
        )
    except Exception:
        logger.exception("Error publishing home tab")
