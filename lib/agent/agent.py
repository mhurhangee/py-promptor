from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage

from config.settings import AI_MODEL


def create_agent(
    model: str = AI_MODEL["id"],
    max_output_tokens: int = AI_MODEL["max_output_tokens"],
    temperature: float = AI_MODEL["temperature"],
    system_message: str = AI_MODEL["system_message"],
    session_id: str = "",
) -> Agent:
    return Agent(
        model=OpenAIChat(
            id=model,
            temperature=temperature,
            max_completion_tokens=max_output_tokens,
        ),
        session_id=session_id,
        markdown=True,
        system_message=system_message,
        storage=SqliteStorage(table_name="agent_sessions", db_file="data/promptor.db", auto_upgrade_schema=True),
        add_history_to_messages=True,  # Include history in messages
    )
