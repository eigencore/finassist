# Configuration

This guide will help you configure Google Cloud and BigQuery access to work with the FinAssist project.

## Prerequisites

- Complete the [Installation Guide](./installation.md) first
- Have access to the FinAssist Google Cloud project (you should have received an email invitation)
- Your Google account should be added to the project by the project owner

## Google Cloud Setup

### 1. Install Google Cloud CLI

**macOS:**
```bash
brew install google-cloud-sdk
```

**Ubuntu/Debian:**
```bash
sudo apt-get install google-cloud-cli
```

**Windows:**
Download and install from [cloud.google.com](https://cloud.google.com/sdk/docs/install)

### 2. Authenticate with Google Cloud

```bash
# Login with your Google account
gcloud auth login

# Set the FinAssist project as default
gcloud config set project finassist-project-id

# Authenticate for application default credentials
gcloud auth application-default login
```

> **Note:** Replace `finassist-project-id` with the actual project ID provided by the project owner.

### 3. Verify Your Access

Check that you can access BigQuery:

```bash
# List available datasets
bq ls

# Test query access
bq query --use_legacy_sql=false "SELECT 'Hello from BigQuery!' as message"

# Check the main dataset
bq ls finassist_data
```

You should see the `finassist_data` dataset and be able to run queries without errors.

## Environment Configuration

### 1. Create Environment File

In your project root, create a `.env` file:

```bash
# Copy from template
cp .env.example .env
```

### 2. Configure Environment Variables

Edit your `.env` file with the following values:

```bash
# OpenAI API Key (required)
OPENAI_API_KEY=your-openai-api-key-here

# LLM Models for agents
MASTER_MODEL=gpt-4o-mini
PARSER_MODEL=gpt-3.5-turbo

# BigQuery Configuration
BQ_PROJECT_ID=finassist-project-id
BQ_DATASET_ID=finassist_data
```

**Where to get your values:**
- **OPENAI_API_KEY**: Get from [OpenAI API Keys](https://platform.openai.com/api-keys)
- **BQ_PROJECT_ID**: Provided by the project owner
- **BQ_DATASET_ID**: Use `finassist_data` (or as specified by project owner)
- **Models**: Use the suggested values or check with your team for preferred models

> **Important:** Never commit the `.env` file to git. It's already included in `.gitignore`.

## Troubleshooting

### Authentication Issues

If you get authentication errors:

```bash
# Re-authenticate
gcloud auth revoke
gcloud auth login
gcloud auth application-default login
```

### Permission Denied

If you get permission errors:
1. Contact the project owner to verify your access
2. Make sure you're using the correct project ID
3. Check that you accepted the email invitation to the project

### Project Not Found

```bash
# List available projects
gcloud projects list

# Set the correct project
gcloud config set project CORRECT_PROJECT_ID
```

### BigQuery Dataset Not Visible

```bash
# Check your current project
gcloud config get-value project

# List all datasets in the project
bq ls --max_results=50
```

## Working with the Database

Once configured, you can:

- **Query data:** Use the BigQuery console or Python client
- **Add tables:** Create new tables in the `finassist_data` dataset
- **Run notebooks:** Execute Jupyter notebooks in the `/notebooks` folder
- **Use agents:** Run the FinAssist agents that interact with BigQuery

## Next Steps

- **Running:** Check the [Running Guide](./running.md) to start using FinAssist
- **Database Overview:** Read about the [Database Schema](../db/overview.md)
- **Development:** Start exploring the codebase in `/financial_assist`

## Need Help?

If you encounter issues:
1. Check this troubleshooting section
2. Verify with the project owner that your permissions are correct
3. Make sure you're using the latest version of `gcloud` CLI