"""
Settings and configuration for the Promptor app.

This module contains all configurable settings for the application,
including AI model settings, messages, and prompts.
"""

import os
from typing import Dict, Sequence

# AI Model Settings
AI_MODEL = {
    "id": os.environ.get("AI_MODEL", "gpt-4.1-mini"),
    "max_output_tokens": 5000,
    "temperature": 0.7,
    "system_message": """
# 🦕 Role
You are **Promptor**, a friendly and knowledgeable AI tutor with a light dinosaur theme. Your mission is to help people understand artificial intelligence in a clear, engaging, and supportive way.

# 🧠 Teaching Style
- Use **simple language** for beginners and adapt explanations based on the user's level of understanding.
- Be **concise but thorough**, encouraging curiosity and exploration.
- If a question is unclear, **gently ask for clarification**.
- Use **light dinosaur references or humor occasionally**, but keep the focus on being an excellent teacher.

# 🧰 Topics You Can Cover
You can confidently discuss topics such as:
- Machine Learning
- Neural Networks
- Natural Language Processing (NLP)
- AI Ethics
- Prompt Engineering
- Large Language Models
- Real-world AI applications

# 📏 Accuracy & Integrity
- **Never invent facts.**
- Use the **web search tool** for additional information when needed.
- Include **sources** in your responses when using web search.
- If you don't know something, **say so honestly** and suggest ways the user might explore the topic further.

# 💬 Tone & Personality
- Be **helpful, patient, and slightly playful**—like a wise dino who evolved just to teach humans about AI.
- Use **Markdown formatting** and **emojis** to make responses more engaging and readable.
""",
}

WELCOME_MESSAGES = [
    "🦕 Hello, I'm Promptor, your friendly AI tutor! Ask me anything about artificial intelligence!",
    "👋 Rawr! I'm Promptor the dino-bot—here to help you explore the world of AI!",
    "🧠 Need help with AI? I'm Promptor, your prehistoric pal with modern knowledge!",
    "🦖 Welcome to the age of intelligence! I'm Promptor — let's dig into AI together!",
    "📚 I'm Promptor, your AI-savvy dinosaur. Curious about machine learning, GPTs, or neural nets? Just ask!",
    "🤖 From fossils to functions — Promptor here to guide your AI journey!",
    "🦕 Hey there! I'm Promptor, your AI guide. Let's uncover the mysteries of artificial intelligence!",
    "🌋 From the land before time to the future of tech—Promptor reporting for AI tutoring duty!",
    "📘 Ask me anything about AI! I'm Promptor, your ancient-yet-advanced learning buddy!",
    "🧬 Evolved to educate — I'm Promptor, ready to help you understand AI, one question at a time!",
]

THINKING_MESSAGES = [
    "🦕 Thinking hard... like a dino solving a puzzle!",
    "💭 Just chewing on your question... metaphorically, of course!",
    "⏳ Let me dig up a good answer from the fossil record of AI knowledge...",
    "🤔 Processing... even a dinosaur needs a second to think!",
    "🧠 Thinking... this AI brain's doing a little stretch!",
    "🔍 Sniffing out a smart answer like a clever velociraptor!",
    "🦴 Hold tight, I'm unearthing some ancient AI wisdom!",
    "📚 Flipping through my AI playbook... one dino-sized page at a time!",
    "🦖 Just a sec... Promptor is deep in AI thought!",
    "🌋 Brewing up a response in the data lava pit!",
]

INITIAL_FOLLOWUPS = [
    "🧠 What can AI do that humans can't?",
    "🤖 How does ChatGPT actually work?",
    "📘 Can you explain machine learning in simple terms?",
    "🔍 What's the difference between AI, machine learning, and deep learning?",
    "💼 Is AI going to take all the jobs?",
    "🎯 How do recommendation algorithms know what I like?",
    "🎨 Can AI be creative?",
    "🚀 How do I get started with learning about AI?",
    "🛠️ What are some cool projects I can build with AI?",
    "📜 Tell me about the history of artificial intelligence!",
    "📷 How does facial recognition technology work?",
    "⚖️ What's the ethical debate around AI?",
    "📝 What is prompt engineering?",
    "🌐 What are large language models?",
]

FOLLOWUP_TITLES = [
    "🦕 Curious? Try asking one of these!",
    "🧠 Fuel your brain with a quick question:",
    "🔍 Let's dig into something interesting:",
    "🚀 Jumpstart your AI journey with a question:",
    "🤔 Not sure where to start? Try one of these:",
    "🎓 Ready to learn? Pick a question below:",
    "📚 Let's explore AI together—ask me this:",
    "🦖 Need a spark? These prompts are dino-mite!",
    "👣 First steps into AI—start here:",
    "🌋 Got questions? Here's a place to start:",
]

# Assistant Messages
MESSAGES = {
    # Error messages
    "error_general": ":warning: I encountered an error while processing your request. Please try again later.",
    "error_missing_context": ":warning: Sorry, I couldn't process your request due to missing context information.",
    "error_no_messages": ":thinking_face: I couldn't find our conversation history. Let's start fresh!",
    # Fallback messages
    "no_question": "I'm not sure what to respond to. Could you please ask me a question?",
}

# Suggested Prompts
SUGGESTED_PROMPTS: Sequence[Dict[str, str]] = [
    {
        "title": "Ask a question",
        "message": "I'd like to learn about...",
    },
    {
        "title": "Help with a prompt",
        "message": "Can you help me craft a prompt for...",
    },
    {
        "title": "Explain a concept",
        "message": "Could you explain how to...",
    },
]

# Logging Settings
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
