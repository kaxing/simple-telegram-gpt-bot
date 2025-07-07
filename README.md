# Simple Telegram GPT Bot

A simple Telegram bot that uses GPT models for chat and personality tests.

## Features

- Chat with GPT models
- Personality tests
- Error handling and graceful shutdown
- Comprehensive test coverage

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `OPENAI_API_KEY`: Your OpenAI API key

## Running Tests

To run tests:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=. --cov-report=html
```

## Available Commands

- `/start` - Start the bot
- `/help` - Show available commands
- `/test` - Start personality test
- `/reset` - Reset settings
- `/clear` - Clear chat history
- `/set` - Change settings
- `/show` - Show session data

## Development

### Adding New Tests

1. Create test file in `tests/` directory
2. Name file as `test_*.py`
3. Create test class inheriting from `unittest.TestCase`
4. Add test methods starting with `test_`

### Running Tests Locally

1. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run tests:
   ```bash
   pytest
   ```

## License

MIT License

### One-click to start
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/sNYhKQ?referralCode=IkBkb-)

---
### References
- [Obtain Your Bot Token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
- [Where do I find my API key?](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)
