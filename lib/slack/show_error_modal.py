from slack_sdk import WebClient

from lib.slack import get_view_id
from lib.ui.error_modal_view import error_modal_view


def show_error_modal(client: WebClient, body: dict, error: str) -> None:
    view_id = get_view_id(body)

    # Use the error_modal_view builder function
    error_view = error_modal_view(error)

    client.views_update(view_id=view_id, view=error_view)
