from slack_sdk import WebClient

from lib.slack import get_view_id


def error_modal(client: WebClient, body: dict, error: str) -> None:
    view_id = get_view_id(body)

    error_view = {
        "type": "modal",
        "callback_id": "error_modal",
        "private_metadata": str(error),
        "title": {"type": "plain_text", "text": "Error", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"❌ *Error:* {error}"
                }
            },
        ],
        "submit": {"type": "plain_text", "text": "Close", "emoji": True},
        "close": {"type": "plain_text", "text": "Close", "emoji": True},
    }

    client.views_update(view_id=view_id, view=error_view)
