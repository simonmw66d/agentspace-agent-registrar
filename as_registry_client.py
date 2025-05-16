import argparse
import json
import os
from as_agent_registry_service import (
    create_agent,
    list_agents,
    get_agent,
    update_agent,
    get_agent_by_display_name,
)

DEFAULT_CONFIG_FILE = "config.json"


def load_config(config_file):
    if not config_file:
        return {}
    
    config_path = os.path.expanduser(config_file)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def get_parameter(name, config, args, prompt=None):
    # Command-line arguments take precedence
    if hasattr(args, name) and getattr(args, name) is not None:
        return getattr(args, name)

    # Then check the config file
    if name in config:
        return config[name]

    # Finally, prompt the user if necessary
    if prompt:
        value = input(f"{prompt}: ")
        if value:
            return value

    return None


def main():
    parser = argparse.ArgumentParser(description="Agent Registry Client")
    parser.add_argument(
        "action",
        choices=["create", "list", "get", "update", "get_by_name"],
        help="Action to perform",
    )
    parser.add_argument("--config", help="Path to the config file", default=DEFAULT_CONFIG_FILE)
    parser.add_argument("--project_id", help="Google Cloud Project ID")
    parser.add_argument("--app_id", help="App ID")
    parser.add_argument("--display_name", help="Agent display name")
    parser.add_argument("--description", help="Agent description")
    parser.add_argument("--tool_description", help="Tool description")
    parser.add_argument("--adk_deployment_id", help="ADK deployment ID")
    parser.add_argument("--auth_id", help="Authorization ID")
    parser.add_argument("--agent_id", help="Agent ID (for get and update)")

    args = parser.parse_args()

    config = load_config(args.config)

    action = args.action

    if action == "create":
        project_id = get_parameter(
            "project_id", config, args, "Enter Google Cloud Project ID"
        )
        app_id = get_parameter("app_id", config, args, "Enter App ID")
        display_name = get_parameter(
            "display_name", config, args, "Enter agent display name"
        )
        description = get_parameter(
            "description", config, args, "Enter agent description"
        )
        tool_description = get_parameter(
            "tool_description", config, args, "Enter tool description"
        )
        adk_deployment_id = get_parameter(
            "adk_deployment_id", config, args, "Enter ADK deployment ID"
        )
        auth_id = get_parameter("auth_id", config, args, "Enter authorization ID")

        if not all(
            [
                project_id,
                app_id,
                display_name,
                description,
                tool_description,
                adk_deployment_id,
                auth_id,
            ]
        ):
            print("Missing required parameters for create action.")
            return

        result = create_agent(
            project_id,
            app_id,
            display_name,
            description,
            tool_description,
            adk_deployment_id,
            auth_id,
        )
        print(json.dumps(result, indent=2))

    elif action == "list":
        project_id = get_parameter(
            "project_id", config, args, "Enter Google Cloud Project ID"
        )
        app_id = get_parameter("app_id", config, args, "Enter App ID")

        if not all([project_id, app_id]):
            print("Missing required parameters for list action.")
            return

        result = list_agents(project_id, app_id)
        print(json.dumps(result, indent=2))

    elif action == "get":
        project_id = get_parameter(
            "project_id", config, args, "Enter Google Cloud Project ID"
        )
        app_id = get_parameter("app_id", config, args, "Enter App ID")
        agent_id = get_parameter("agent_id", config, args, "Enter Agent ID")

        if not all([project_id, app_id, agent_id]):
            print("Missing required parameters for get action.")
            return

        result = get_agent(project_id, app_id, agent_id)
        print(json.dumps(result, indent=2))

    elif action == "update":
        project_id = get_parameter(
            "project_id", config, args, "Enter Google Cloud Project ID"
        )
        app_id = get_parameter("app_id", config, args, "Enter App ID")
        agent_id = get_parameter("agent_id", config, args, "Enter Agent ID")
        display_name = get_parameter(
            "display_name", config, args, "Enter new display name (leave blank to keep current)"
        )
        description = get_parameter(
            "description", config, args, "Enter new description (leave blank to keep current)"
        )
        tool_description = get_parameter(
            "tool_description", config, args, "Enter new tool description (leave blank to keep current)"
        )
        adk_deployment_id = get_parameter(
            "adk_deployment_id", config, args, "Enter new ADK deployment ID (leave blank to keep current)"
        )
        auth_id = get_parameter(
            "auth_id", config, args, "Enter new authorization ID (leave blank to keep current)"
        )

        if not all([project_id, app_id, agent_id]):
            print("Missing required parameters for update action.")
            return

        result = update_agent(
            project_id,
            app_id,
            agent_id,
            display_name,
            description,
            tool_description,
            adk_deployment_id,
            auth_id,
        )
        print(json.dumps(result, indent=2))

    elif action == "get_by_name":
        project_id = get_parameter(
            "project_id", config, args, "Enter Google Cloud Project ID"
        )
        app_id = get_parameter("app_id", config, args, "Enter App ID")
        display_name = get_parameter(
            "display_name", config, args, "Enter agent display name"
        )

        if not all([project_id, app_id, display_name]):
            print("Missing required parameters for get_by_name action.")
            return

        result = get_agent_by_display_name(project_id, app_id, display_name)
        print(json.dumps(result, indent=2))

    else:
        print(f"Invalid action: {action}")


if __name__ == "__main__":
    main()