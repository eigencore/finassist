# Running the Project

This guide shows you how to run FinAssist locally using the Agent Development Kit (ADK).

## Prerequisites

- Complete the [Installation Guide](./installation.md)
- Complete the [Configuration Guide](./configuration.md)
- Ensure your `.env` file is properly configured

## Quick Start

The easiest way to run the project locally is using Google ADK:

```bash
# Activate your poetry environment
poetry shell

# Run the web interface
adk web
```

This will start the FinAssist web interface where you can interact with the multi-agent system.


## Using the Web Interface

Once `adk web` is running, you'll be able to:

1. **Interact with FinAssist agents** through a web-based chat interface
2. **Input financial data** using natural language (e.g., "I paid $50 for groceries yesterday")


## Troubleshooting

### ADK Command Not Found

If `adk web` doesn't work:

```bash
# Install ADK if not available
pip install google-adk

# Or check if it's available in your poetry environment
poetry run adk web
```

### Port Already in Use

If you get a port conflict:

```bash
# Try running on a different port
adk web --port 8080
```

### Environment Variables Not Loading

```bash
# Make sure you're in the project root directory
pwd

# Check if .env file exists
ls -la .env

# Load environment manually if needed
source .env
```

### BigQuery Permission Errors

```bash
# Re-authenticate if needed
gcloud auth application-default login

# Verify project access
gcloud config get-value project
bq ls
```

## Working with FinAssist

### Example Interactions

Once the web interface is running, try these example prompts:

**Adding Transactions:**
- "I spent $25 on lunch today"
- "Yesterday I received my salary of $3000"
- "I paid $120 for my phone bill"


## Next Steps

- Explore the [Database Overview](../db/overview.md) to understand the data structure
- Check out the [Architecture Documentation](../README.md) to learn about the multi-agent system
- Start experimenting with different financial queries and scenarios

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your configuration following the [Configuration Guide](./configuration.md)
3. Make sure all prerequisites are installed from the [Installation Guide](./installation.md)
4. Contact the project maintainer if problems persist