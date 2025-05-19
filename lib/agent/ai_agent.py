"""
AI Agent implementation using Agno framework.

This module provides the AI functionality for the Promptor app
using the Agno framework and OpenAI models.
"""

from typing import Dict, List

from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIResponses

from config.settings import AI_MODEL, MESSAGES


class AIAgent:
    """
    AI Agent class that handles interactions with the Agno framework.
    """

    def __init__(self, model_id: str | None = None):
        """
        Initialize the AI Agent with the specified model.

        Args:
            model_id: The ID of the OpenAI model to use (defaults to config setting)
        """
        # Use the provided model_id or fall back to the configured model
        model = model_id or AI_MODEL["id"]
        self.agent = Agent(
            model=OpenAIResponses(
                id=model,
                max_output_tokens=AI_MODEL["max_output_tokens"],
                temperature=AI_MODEL["temperature"],
            ),
            markdown=True,
            system_message=AI_MODEL["system_message"],
        )

    def get_response(self, message: str) -> str:
        """
        Get a response from the AI agent for the given message.

        Args:
            message: The user's message to respond to

        Returns:
            The AI's response as a string
        """
        try:
            # Get the response from the AI agent
            response: RunResponse = self.agent.run(message)
            return response.content or "I don't have a response at this time."
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def process_conversation(self, messages: List[Dict[str, str]]) -> str:
        """
        Process a conversation and return an AI response.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys

        Returns:
            The AI's response as a string
        """
        # For now, we're just responding to the last user message
        # In the future, we can use the full conversation history
        for message in reversed(messages):
            if message.get("role") == "user":
                return self.get_response(message.get("content", ""))

        return MESSAGES["no_question"]


# Create a singleton instance for easy import
ai_agent = AIAgent()
