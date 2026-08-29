# Calling LLMs in Python

This project demonstrates three ways to interact with OpenAI language models using Python and `gpt-4o-mini`.

## Methods Covered

1. **REST API** — Sends an HTTP POST request using the `requests` library.
2. **OpenAI SDK** — Uses the official OpenAI Python SDK.
3. **LangChain** — Uses LangChain's `ChatOpenAI` wrapper.

## Setup

1. Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

## Run Examples

```bash
uv run python main01.py  # REST API
uv run python main02.py  # OpenAI SDK
uv run python main03.py  # LangChain
```

> Never commit your `.env` file or API key to GitHub.