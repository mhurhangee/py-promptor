"""Agent for improving prompts."""
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from config.settings import AI_MODEL
from lib.agent.improve_prompt_schema import ImprovePromptSchema

# System message for the improve prompt agent
system_message = """You are a prompt engineering expert who specializes in improving prompts for AI systems.
Your task is to analyze the given prompt and provide an improved version that is:

1. Clearer and more specific
2. Better structured with a logical flow
3. More effective at eliciting the desired response
4. Free of unnecessary content or redundancies

Additionally, provide a brief explanation of your improvements and why they make the prompt more effective.

Focus on making meaningful improvements while preserving the original intent of the prompt.
"""


def create_improve_prompt_agent(session_id: str = "") -> Agent:
    """Create an agent for improving prompts.

    Args:
        session_id: Optional session ID for the agent

    Returns:
        An Agent configured for improving prompts
    """
    return Agent(
        model=OpenAIChat(
            id=AI_MODEL["id"],
            temperature=0.4,
            max_completion_tokens=1000,
        ),
        session_id=session_id,
        markdown=False,
        system_message=system_message,
        add_history_to_messages=False,
        response_model=ImprovePromptSchema,
        use_json_mode=True,
    )
