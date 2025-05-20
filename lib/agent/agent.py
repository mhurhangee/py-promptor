from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage

from config.settings import AI_MODEL

from .schema import ResponseSchema


def create_agent(
    session_id: str = "",
) -> Agent:
    return Agent(
        model=OpenAIChat(
            id=AI_MODEL["id"],
            temperature=AI_MODEL["temperature"],
            max_completion_tokens=AI_MODEL["max_output_tokens"],
        ),
        session_id=session_id,
        markdown=True,
        system_message=AI_MODEL["system_message"],
        storage=SqliteStorage(table_name="agent_sessions", db_file="data/promptor.db", auto_upgrade_schema=True),
        add_history_to_messages=True,  # Include history in messages
        response_model=ResponseSchema,
        use_json_mode=True,
    )
