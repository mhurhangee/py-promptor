def get_user_id(body: dict) -> str:
    """Get the user ID from the body."""
    return body.get("user", {}).get("id")
