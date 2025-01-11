![GitHub stars](https://img.shields.io/github/stars/02tYasui/slackbot.svg)
![Contributors](https://img.shields.io/github/contributors/02tYasui/slackbot)
![GitHub License](https://img.shields.io/github/license/02tyasui/slackbot)

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

This SlackBot leverages OpenAI API to manage thread history and provides seamless AI integration within Slack. Key features include:

- **Thread History Management**: Automatically tracks all interactions within Slack threads, enabling context-aware AI responses.
- **OpenAI API Integration**: Utilizes OpenAI's powerful capabilities to generate high-quality, relevant responses.
- **Easy Setup**: Simple setup process using environment variables for quick integration with any Slack workspace.
- **Mention Response**: Automatically responds when mentioned, allowing team members to directly ask questions or request specific tasks.
  To enable this feature, configure the bot in the Slack API dashboard and add appropriate event subscriptions to detect mentions.

## Slack Configuration
#### OAuth Scope
```text
app_mentions:read
chat:write
im:history
im:read
im:write
```

#### Event Subscriptions
```text
app_mention
app_mentions:read
message.im
```

## Getting Started

You can run the project using either pipenv or Docker (recommended).

Create a `.env` file in the project root directory and add the following environment variables:
Refer to `.env.dev` for guidance.
```Dotenv
# Environment
ENVIRONMENT=dev

# OpenAI API
MODEL_NAME=gpt-4o-mini
OPENAI_API_KEY=your_openai_api_key

# Slack
SLACK_APP_TOKEN=your_slack_app_token
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_BOT_ID=your_slack_bot_id

# DynamoDB (for production chat history)
DYNAMODB_TABLE_NAME=chat-history
AWS_REGION=ap-northeast-1

# Tools Configuration
ENABLE_SEARCH=true
ENABLE_VECTOR=true

# Langsmith
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
