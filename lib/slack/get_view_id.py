def get_view_id(body: dict) -> str:
    """Get the view ID from the body."""
    return body.get("container", {}).get("view_id")
