r![GitHub stars](https://img.shields.io/github/stars/02tYasui/langchain-slackbot.svg)
![Contributors](https://img.shields.io/github/contributors/02tYasui/langchain-slackbot)
![GitHub License](https://img.shields.io/github/license/02tYasui/langchain-slackbot)

# AI-Powered SlackBot
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-121112?logo=chainlink&logoColor=white)](https://langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com/)
[![Slack](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=white)](https://slack.com/)

## Important Notes

1. Security: Never commit the `.env` file to version control. Ensure it's listed in your `.gitignore` file to prevent accidental exposure of sensitive information.

2. Slack Bot Configuration: This SlackBot operates in Socket Mode. Make sure your Slack app is configured to use Socket Mode in the Slack API dashboard. When generating the `SLACK_APP_TOKEN`, select the Socket Mode option.

## Features

This SlackBot leverages OpenAI API and LangChain to provide intelligent responses within Slack. Key features include:

- **Intelligent Thread Management**: 
  - Automatically preserves conversation context within Slack threads
  - Understands the full thread history for more contextual responses
  - Seamlessly handles multiple concurrent conversations

- **Advanced AI Integration**: 
  - Powered by OpenAI's language models
  - Multiple specialized tools for different tasks:
    - Web Search: Access to current information
    - Vector Search: Query internal documents and guidelines

- **Performance Optimized**:
  - Efficient thread history management using Slack API
  - Configurable timeouts and retry mechanisms
  - Detailed logging for monitoring and debugging

- **Easy Setup**: 
  - Simple configuration through environment variables
  - Docker support for easy deployment
  - Flexible tool enabling/disabling

## Slack Configuration

### OAuth Scopes
```text
app_mentions:read
channels:history
chat:write
groups:history
im:history
im:read
im:write
```

### Event Subscriptions
```text
app_mention
message.groups
message.im
```

## Getting Started

You can run the project using either pipenv or Docker (recommended).

Create a `.env` file in the project root directory and add the following environment variables:
Refer to `.env.dev` for guidance.
```Dotenv
# Environment
ENVIRONMENT=dev
DEBUG=false           # Enable detailed error messages

# OpenAI API
MODEL_NAME=gpt-4     # Or gpt-3.5-turbo
OPENAI_API_KEY=your_openai_api_key
MODEL_TEMPERATURE=0   # 0-1, lower for more focused responses
MODEL_TIMEOUT=30     # Seconds
MAX_AGENT_ITERATIONS=3

# Slack
SLACK_APP_TOKEN=your_slack_app_token
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_BOT_ID=your_slack_bot_id
API_TIMEOUT=60       # Slack API timeout

# Vector Store Configuration
VECTOR_STORE_PATH=./vector_store
VECTOR_CHUNK_SIZE=100
VECTOR_CHUNK_OVERLAP=20
VECTOR_DOC_PATH=./vector_file/sample.txt

# Tools Configuration
ENABLE_SEARCH=true
ENABLE_VECTOR=true

# Langsmith (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=your_project_name
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### Using pipenv
1. Install pipenv: `pip install pipenv`

2. Clone the repository:
```bash
git clone https://github.com/02tYasui/slackbot.git
cd slackbot
```

3. Install project dependencies using pipenv:
```bash
pipenv install
```

4. Activate pipenv environment:
```bash
pipenv shell
```

5. Run the SlackBot:
```bash
python src/app.py
```

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/02tYasui/slackbot.git
cd slackbot
```

2. Build and run Docker container:
```bash
docker compose up --build
```

## System Architecture

The bot uses the following components:

1. **Slack Integration**:
   - Socket Mode for real-time communication
   - Thread history tracking for context awareness
   - Automatic mention detection and response

2. **Language Model**:
   - OpenAI's GPT models for natural language processing
   - Configurable temperature and timeout settings
   - Error handling and retry mechanisms

3. **Tools**:
   - Web Search: DuckDuckGo integration for current information
   - Vector Search: Document retrieval using ChromaDB
   - Customizable tool configuration via environment variables

4. **Logging and Monitoring**:
   - Detailed logging with file and line information
   - Performance metrics tracking
   - Debug mode for development

## Error Handling

The bot includes comprehensive error handling:

- API timeouts and retry logic
- Invalid input detection
- Detailed error logging
- User-friendly error messages
- Debug mode for development

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
