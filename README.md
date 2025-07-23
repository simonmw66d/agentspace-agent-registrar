# AgentSpace Agent Registrar

A modern, refactored command-line interface for managing agents in both **Agent Engine** (Vertex AI Agent Engine) and **Agentspace** (Agent Gallery). This tool provides a clean, maintainable interface with improved error handling and configuration management.

## ✨ What's New in This Fork

- **CLI Framework**: Built with Typer for better UX and help generation
- **HTTP Client**: Uses `httpx` instead of `curl` subprocess calls
- **Type Safety**: Pydantic models for configuration validation
- **Error Handling**: Custom exceptions and graceful error recovery
- **Dependency Management**: Uses `uv` for dependency management

## 🚀 Quick Start

### Prerequisites

1. **Google Cloud SDK (gcloud)**: Ensure you have the Google Cloud SDK installed and initialized
2. **Python 3.12+**: Required for the new package structure
3. **uv**: Modern Python package manager (recommended) or pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd agentspace-agent-registrar

# Install dependencies using uv (recommended)   
uv sync

# Or using pip
pip install -e .
```

### Basic Usage

```bash
# Show available commands
uv run python -m agentspace_registrar.cli.main --help

# List all subcommands
uv run python -m agentspace_registrar.cli.main registry --help
uv run python -m agentspace_registrar.cli.main engine --help
uv run python -m agentspace_registrar.cli.main auth --help
```

## 📁 Project Structure

```
agentspace-agent-registrar/
├── src/
│   └── agentspace_registrar/
│       ├── cli/
│       │   ├── commands/
│       │   │   ├── registry.py      # Agent Registry commands
│       │   │   ├── engine.py        # Agent Engine commands
│       │   │   └── auth.py          # Authorization commands
│       │   ├── base.py              # Base command classes
│       │   └── main.py              # CLI entry point
│       ├── services/
│       │   ├── agent_registry.py    # Agent Registry service (httpx-based)
│       │   ├── agent_engine.py      # Agent Engine service
│       │   └── authorization.py     # Authorization service
│       ├── config/
│       │   ├── manager.py           # Configuration management
│       │   └── models.py            # Pydantic configuration models
│       ├── utils/
│       │   ├── auth.py              # Authentication utilities
│       │   └── output.py            # Output formatting
│       └── exceptions.py            # Custom exceptions
├── pyproject.toml                   # Project configuration
└── README.md
```

## ⚙️ Configuration

The new CLI supports multiple configuration sources with the following precedence (highest to lowest):

1. **Command-line arguments**
2. **Configuration file** (`config.json`)
3. **Environment variables** (with `AGENTSPACE_` prefix)
4. **Interactive prompts**
5. **Default values**

### Configuration File

Create a `config.json` file in your project directory:

```json
{
  "project_id": "your-gcp-project-id",
  "location": "us-central1",
  "app_id": "your-agentspace-app-id",
  "ars_display_name": "My Registered Agent Name",
  "description": "Agent Description for Registry",
  "tool_description": "Tool Description for Registry",
  "adk_deployment_id": "your-reasoning-engine-id",
  "auth_id": "your-oauth-auth-id",
  "api_location": "global",
  "re_location": "global"
}
```

### Environment Variables

You can also use environment variables with the `AGENTSPACE_` prefix:

```bash
export AGENTSPACE_PROJECT_ID="your-gcp-project-id"
export AGENTSPACE_APP_ID="your-agentspace-app-id"
export AGENTSPACE_API_LOCATION="global"
```

## 🎯 Command Reference

### Agent Registry Commands (Agentspace Agent Gallery)

```bash
# Create a new agent
uv run python -m agentspace_registrar.cli.main registry create \
  --project-id your-project \
  --app-id your-app \
  --display-name "My Agent" \
  --description "Agent description" \
  --tool-description "Tool description" \
  --adk-deployment-id your-deployment-id

# List all agents
uv run python -m agentspace_registrar.cli.main registry list \
  --project-id your-project \
  --app-id your-app

# Get a specific agent
uv run python -m agentspace_registrar.cli.main registry get agent-id \
  --project-id your-project \
  --app-id your-app

# Update an agent
uv run python -m agentspace_registrar.cli.main registry update agent-id \
  --project-id your-project \
  --app-id your-app \
  --display-name "Updated Name"

# Get agents by display name
uv run python -m agentspace_registrar.cli.main registry get-by-name "Agent Name" \
  --project-id your-project \
  --app-id your-app

# Delete an agent
uv run python -m agentspace_registrar.cli.main registry delete agent-id \
  --project-id your-project \
  --app-id your-app
```

### Agent Engine Commands (Vertex AI Agent Engine)

```bash
# List all deployed agents
uv run python -m agentspace_registrar.cli.main engine list \
  --project-id your-project \
  --location us-central1

# Get a specific agent
uv run python -m agentspace_registrar.cli.main engine get resource-id \
  --project-id your-project \
  --location us-central1

# List agents by display name
uv run python -m agentspace_registrar.cli.main engine list-by-name "Agent Name" \
  --project-id your-project \
  --location us-central1

# Delete an agent
uv run python -m agentspace_registrar.cli.main engine delete resource-name \
  --project-id your-project \
  --location us-central1
```

### Authorization Commands

```bash
# Create a new authorization
uv run python -m agentspace_registrar.cli.main auth create auth-id \
  --project-id your-project \
  --location us \
  --scopes email

# List all authorizations
uv run python -m agentspace_registrar.cli.main auth list \
  --project-id your-project \
  --location us

# Delete an authorization
uv run python -m agentspace_registrar.cli.main auth delete auth-id \
  --project-id your-project \
  --location us

# Refresh authorization (create new, delete old)
uv run python -m agentspace_registrar.cli.main auth refresh old-auth-id \
  --project-id your-project \
  --location us \
  --new-auth-id new-auth-id
```

## 🔄 Migration from Old CLI

### Old vs New Usage

| Old Command | New Command |
|-------------|-------------|
| `python as_registry_client.py register_agent --project_id x --app_id y` | `uv run python -m agentspace_registrar.cli.main registry create --project-id x --app-id y` |
| `python as_registry_client.py list_registry --project_id x --app_id y` | `uv run python -m agentspace_registrar.cli.main registry list --project-id x --app-id y` |
| `python as_registry_client.py list_deployed_agents --project_id x` | `uv run python -m agentspace_registrar.cli.main engine list --project-id x` |
| `python refresh_authz.py` | `uv run python -m agentspace_registrar.cli.main auth refresh old-id` |

### Key Changes

1. **Command Structure**: Commands are now organized by service (registry, engine, auth)
2. **Parameter Names**: Kebab-case instead of snake_case (e.g., `--project-id` vs `--project_id`)
3. **Configuration**: Better support for config files and environment variables
4. **Error Handling**: More informative error messages and graceful failure
5. **Help**: Comprehensive help for all commands and subcommands

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install in development mode
uv pip install -e .

# Install development dependencies
uv add --group dev mypy ruff

# Run linting
uv run ruff check src/

# Run type checking
uv run mypy src/
```

### Running Tests

```bash
# Run the CLI help to verify installation
uv run python -m agentspace_registrar.cli.main --help
```

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure you have valid Google Cloud credentials
2. **Configuration Not Found**: Check that your `config.json` exists and is valid JSON
3. **Permission Errors**: Verify you have the necessary IAM permissions for the services

### Debug Mode

Enable debug logging by setting the environment variable:

```bash
export PYTHONPATH=src
export LOG_LEVEL=DEBUG
uv run python -m agentspace_registrar.cli.main registry list --project-id your-project --app-id your-app
```