from .get_action_id import get_action_id


def get_prompt_id(body: dict) -> int:
    """Get the prompt ID from the body."""
    action_id = get_action_id(body)
    if action_id and ":" in action_id:
        return int(action_id.split(":")[1])
    return 0
