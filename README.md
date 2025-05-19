# Promptor - AI Tutor and Prompt Library for Slack

<img src="promptor.webp" alt="Promptor" width="500" />

Promptor is a Slack-first AI assistant that helps teams with AI-powered tutoring and prompt management. Built with Python and the Slack Bolt framework, it provides a seamless AI experience within your Slack workspace.

## Features

- 🎓 AI-powered tutoring and assistance
- 📚 Prompt library management
- 🧵 Threaded conversations for better context
- ⚡ Real-time responses using OpenAI's technology
- 🔄 Seamless Slack integration

## Installation

### Prerequisites
- Python 3.8+
- A Slack workspace where you have permission to install apps
- [ngrok](https://ngrok.com/) for local development (recommended)

### 1. Create a Slack App
1. Go to [Slack API](https://api.slack.com/apps/new) and select "From an app manifest"
2. Choose your workspace
3. Copy the contents of [manifest.json](./manifest.json) into the manifest editor
4. Click *Next* and review the configuration
5. Click *Create* and then *Install to Workspace*

### 2. Set Up Environment

```bash
# Clone the repository
git clone https://github.com/your-username/py-promptor.git
cd py-promptor

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Configure Environment Variables

1. Get your tokens from the Slack API dashboard:
   - **Bot User OAuth Token** (starts with `xoxb-`)
   - **App-Level Token** (starts with `xapp-`)

2. Set environment variables
```
export SLACK_BOT_TOKEN=xoxb-your-bot-token
export SLACK_APP_TOKEN=xapp-your-app-token
export OPENAI_API_KEY=your-openai-api-key
```

### 4. Run the Application

```bash
# Start the app
python3 app.py
```

## Development

### Linting and Formatting

```bash
# Run flake8 for linting
flake8 .

# Format code with black
black .

# Sort imports with isort
isort .
```

### Testing

Run the test suite with:
```bash
pytest
```

## Project Structure

- `app.py` - Main application entry point
- `manifest.json` - Slack app configuration
- `requirements.txt` - Python dependencies
- `/listeners` - Event handlers organized by type