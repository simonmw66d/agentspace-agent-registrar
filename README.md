# Agent Registry Client - README

This client provides a command-line interface to interact with the Agent Registry service, allowing you to manage agents in Agentspace's Agent Gallery.

## Prerequisites

1.  **Google Cloud SDK (gcloud):**  Ensure you have the Google Cloud SDK installed and initialized.  You can download it from [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install).
2.  **Agent Pre-deployment:** The agent must be pre-deployed to Agent Engine. The Reasoning Engine ID from this deployment will be required.
3.  **Python 3.7+:**  Python 3.7 or a later version is required.  You can check your Python version with `python3 --version`.
4.  **Virtual Environment (Recommended):** It's highly recommended to use a virtual environment to isolate project dependencies. You can create and activate one like this:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    # .venv\Scripts\activate  # On Windows
    ```

## Setup

1.  **Clone the repository:**  If you haven't already, clone the repository containing the client code.
2.  **Navigate to the directory:** Change your current directory to the location of the `as_registry_client.py` script.
3.  **(Optional) Install dependencies:** If your project has any dependencies (beyond the standard library), install them using `pip`:

    ```bash
    # If you have a requirements.txt file:
    pip install -r requirements.txt
    ```

## Configuration

You can provide parameters to the client in three ways, with the following precedence (highest to lowest):

1.  **Command-line arguments:** Parameters passed directly when running the script.
2.  **Configuration file (`config.json`):** A JSON file containing default parameter values.
3.  **Interactive input:** The client will prompt you for any missing parameters.

**To use a configuration file:**

1.  Create a file named `config.json` in the same directory as `as_registry_client.py`.
2.  Use the following template, replacing the placeholder values with your actual configuration:

    ```json
    {
        "project_id": "your_project_id",
        "app_id": "your_app_id",
        "display_name": "Agent Name",
        "description": "Agent Description",
        "tool_description": "Tool Description",
        "adk_deployment_id": "your_deployment_id",
        "auth_id": "your_auth_id",
        "agent_id": "your_agent_id"
    }
    ```

## Usage

The basic syntax for running the client is:

```bash
python as_registry_client.py [action] [options]
```

If you don't provide the `action` on the command line, the client will prompt you to enter it.

### Actions

The following actions are supported:

*   **`create`:** Creates a new agent.
*   **`list`:** Lists existing agents.
*   **`get`:** Retrieves details for a specific agent.
*   **`update`:** Updates an existing agent.
*   **`get_by_name`:** Retrieves an agent by its display name.

### Options

The following options can be used to provide parameters:

*   `--config <path>`: Specifies the path to the configuration file (defaults to `config.json`).
*   `--project_id <project_id>`: Your Google Cloud Project ID.
*   `--app_id <app_id>`: The App ID for your Discovery Engine.
*   `--display_name <display_name>`: The display name of the agent.
*   `--description <description>`: A description of the agent.
*   `--tool_description <tool_description>`: A description of the tool used by the agent.
*   `--adk_deployment_id <adk_deployment_id>`: The Reasoning Engine ID (obtained after deploying the agent to Agent Engine).
*   `--auth_id <auth_id>`: The authorization ID.
*   `--agent_id <agent_id>`: The ID of the agent (required for `get` and `update` actions).

### Examples

**1. Create an agent (using interactive input):**

```bash
python as_registry_client.py create
```

The client will prompt you for each required parameter.

**2. List agents (using command-line arguments):**

```bash
python as_registry_client.py list --project_id your-project-id --app_id your-app-id
```

**3. Get an agent by ID (using a configuration file and command-line argument):**

```bash
python as_registry_client.py get --agent_id your-agent-id --config my_config.json
```

This will load `project_id` and `app_id` from `my_config.json` and use the provided `agent_id`.

**4. Update an agent (partially, using a configuration file and command-line argument):**

```bash
python as_registry_client.py update --agent_id your-agent-id --display_name "New Agent Name"
```

This will update only the `display_name` of the agent with the specified ID, using other parameters from `config.json` or prompting the user if not found.