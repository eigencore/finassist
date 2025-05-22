# Installation

## Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Poetry** - [Install Poetry](https://python-poetry.org/docs/#installation)
- **Git** - [Install Git](https://git-scm.com/downloads)

## Fork the Repository

1. Navigate to the [FinAssist repository](https://github.com/eigencore/finassist)
2. Click the **Fork** button in the top-right corner
3. Select your GitHub account to create a fork

## Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/finassist.git
cd finassist
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Install Dependencies

The project uses Poetry for dependency management:

```bash
# Install all project dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Verify Installation

Test that everything is working correctly:

```bash
# Check if the main module can be imported
poetry run python -c "import financial_assist; print('✅ FinAssist installed successfully!')"
```

## Next Steps

- **Configuration**: See [Configuration Guide](./configuration.md) for Google Cloud setup
- **Running**: Check [Running Guide](./running.md) to start using FinAssist
- **Overview**: Read the [Project Overview](../README.md) to understand the architecture