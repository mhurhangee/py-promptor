def get_action_id(body: dict) -> str:
    """Get the action ID from the body."""
    actions = body.get("actions", [])
    return actions[0].get("action_id") if actions else ""
