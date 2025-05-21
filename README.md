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
python -m venv .venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

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

### Package Management with UV

This project uses [UV](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

```bash
# Install dependencies
uv pip install -r requirements.txt

# Add a new package
uv pip install package-name

# Update requirements.txt after adding packages
uv pip freeze > requirements.txt
```

### Linting and Formatting with Ruff

This project uses [Ruff](https://github.com/astral-sh/ruff) for fast Python linting and formatting.

```bash
# Check code with Ruff
ruff check .

# Format code with Ruff
ruff format .

# Fix auto-fixable issues
ruff check --fix .
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
- `/config` - Configuration files
- `/lib` - Library files

## Roadmap

I've carefully considered the features you want to implement to complete the prompt library. Here's a strategic implementation plan that balances technical complexity with user value:

Implementation Order and Approach
1. Private and Public Libraries
Implementation Approach:

Database Schema Updates:
Add is_public boolean field to the Prompt model
Add copied_from_id field to track the origin of copied prompts
UI Components:
Add toggle in prompt detail modal for public/private status
Create a tab-like interface in the home tab to switch between "My Library" and "Public Library"
Add "Save to My Library" button for public prompts
Backend Logic:
Update database queries to filter by public/private status
Add permission checks to ensure users can only modify their own prompts
Implement copying functionality for public prompts
Why First: This feature provides the foundation for sharing and collaboration, which are core to the other features.

2. Sharing Prompts
Implementation Approach:

Share Modal:
Create a share modal with options for channels and users
Include an optional message field for context
Integration Points:
Add "Share" button to prompt detail modal
Implement channel posting functionality
Implement DM sending functionality
Message Format:
Design rich message format that shows prompt details
Include buttons to "Use" or "Save to Library"
Why Second: Once we have public/private functionality, sharing is a natural extension that adds immediate value.

3. Sorting of Prompts
Implementation Approach:

Sorting Options:
Add dropdown for sort options in home tab
Implement sorting by date, name, and favorites (for public library)
Backend Changes:
Update database queries to support different sort orders
Add caching for frequently accessed sort orders
UI Updates:
Add visual indicators for current sort order
Consider adding column headers that can be clicked to sort
Why Third: Sorting becomes more valuable as the library grows, and it's relatively straightforward to implement.

4. Searching and Prompt Suggestions
Implementation Approach:

Basic Search:
Add search bar to home tab
Implement keyword search across title, content, tags, and category
Semantic Search:
Create an Agno agent for semantic search
Index prompts in a knowledge base
Implement relevance scoring
Prompt Suggestions:
Add a message shortcut for suggesting prompts
Create an agent that analyzes message content and suggests relevant prompts
Display suggestions in a modal with options to use or save
Why Fourth: Search becomes more valuable as the library grows, and semantic search builds on the basic functionality.

5. Prompt Templates
Implementation Approach:

Template Syntax:
Define a simple syntax for variables (e.g., {variable_name})
Add parser to identify variables in prompts
UI for Template Usage:
When using a template prompt, show a form with fields for each variable
Pre-populate with default values if available
Template Creation:
Add documentation or hints in the prompt creation modal
Consider adding a "Convert to Template" option
Why Last: This is the most complex feature and requires careful UI design to maintain simplicity.

Technical Considerations
Database Changes
Add is_public boolean to Prompt model (default: false)
Add copied_from_id foreign key to Prompt model (nullable)
Add last_used_at timestamp field for sorting
Consider adding a usage_count field for popularity metrics
UI Components to Create
Library tab switcher (My/Public)
Share modal
Sort dropdown
Search interface
Template variable form
Backend Logic
Permission system for public/private prompts
Sharing functionality
Search indexing and querying
Template variable parsing and substitution
Implementation Timeline
Private/Public Libraries: 1-2 weeks
Database migration
UI updates
Permission system
Sharing Prompts: 1 week
Share modal
Channel/DM integration
Sorting: 2-3 days
Sort options
UI updates
Search and Suggestions: 1-2 weeks
Basic search: 2-3 days
Semantic search: 3-5 days
Prompt suggestions: 3-5 days
Templates: 1 week
Template syntax
Variable form UI
Parsing and substitution
This plan provides a logical progression that builds each feature on top of the previous ones, maximizing user value at each step while managing technical complexity.

Would you like me to elaborate on any specific feature implementation or adjust the priorities?
