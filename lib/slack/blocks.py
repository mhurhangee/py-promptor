def md_section(text: str) -> dict:
    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}


def text_context(text: str) -> dict:
    return {"type": "context", "elements": [{"type": "mrkdwn", "text": text}]}
