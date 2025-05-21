from slack_sdk import WebClient

from lib.slack import get_user_id


def send_error_eph(client: WebClient, body: dict, error: str) -> None:
    user_id = get_user_id(body)
    client.chat_postEphemeral(
        channel=user_id,
        user=user_id,
        text=f"❌ {error}",
    )
