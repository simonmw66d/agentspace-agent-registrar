import argparse
import agent_engine_manager

def get_parameter(name, args, prompt=None, required=False):
    """
    Retrieves a parameter value.
    Checks command-line arguments first, then prompts the user if necessary.
    """
    value = getattr(args, name, None)
    if value is not None:
        return value

    if prompt:
        value = input(f"{prompt}: ")
        if value:
            return value
    
    if required and not value:
        raise ValueError(f"Parameter '{name}' is required.")
    return None

def main():
    parser = argparse.ArgumentParser(description="Agent Engine Manager Client")
    parser.add_argument(
        "action", nargs='?', # Make action optional to allow prompting
        choices=["list", "delete", "get", "list_by_name"],
        help="Action to perform: \n"
             "  list: List all agents.\n"
             "  delete: Delete an agent by resource name.\n"
             "  get: Get an agent by resource ID.\n"
             "  list_by_name: List agents by display name."
    )
    parser.add_argument(
        "--resource_name",
        help="Resource name of the agent (e.g., projects/PROJECT_ID/locations/LOCATION/agents/AGENT_ID). Required for 'delete'."
    )
    parser.add_argument(
        "--resource_id",
        help="Resource ID of the agent. Required for 'get'."
    )
    parser.add_argument(
        "--display_name",
        help="Display name of the agent. Required for 'list_by_name'."
    )

    args = parser.parse_args()

    action = args.action
    if not action:
        action = input(
            "Enter action to perform (list, delete, get, list_by_name): "
        ).strip().lower()
        if action not in ["list", "delete", "get", "list_by_name"]:
            print(f"Invalid action: {action}")
            parser.print_help()
            return

    try:
        if action == "list":
            result = agent_engine_manager.list_agents()
            print(result)
        elif action == "delete":
            resource_name = get_parameter(
                "resource_name", args, 
                prompt="Enter resource name of the agent to delete (e.g., projects/PROJECT_ID/locations/LOCATION/agents/AGENT_ID)",
                required=True
            )
            if not resource_name: # Should be caught by required=True in get_parameter, but as a safeguard
                print("Resource name is required for the 'delete' action.")
                return
            
            confirmation = input(f"Are you sure you want to delete agent with resource name '{resource_name}'? (yes/no): ")
            if confirmation.lower() == "yes":
                result = agent_engine_manager.delete_agent(resource_name)
                print(result)
            else:
                print("Deletion cancelled.")

        elif action == "get":
            resource_id = get_parameter(
                "resource_id", args, 
                prompt="Enter resource ID of the agent to get",
                required=True
            )
            if not resource_id:
                print("Resource ID is required for the 'get' action.")
                return
            result = agent_engine_manager.get_agent(resource_id)
            print(result)

        elif action == "list_by_name":
            display_name = get_parameter(
                "display_name", args, 
                prompt="Enter display name of the agent to list",
                required=True
            )
            if not display_name:
                print("Display name is required for the 'list_by_name' action.")
                return
            result = agent_engine_manager.list_agents_by_display_name(display_name)
            print(result)
        else:
            # This case should ideally not be reached due to 'choices' in add_argument
            print(f"Invalid action: {action}")
            parser.print_help()

    except Exception as e:
        print(f"An error occurred: {e}")
        # You might want to add more specific error handling or logging here
        # For example, if agent_engine_manager functions can raise specific exceptions

if __name__ == "__main__":
    # Note: For agent_engine_manager to work,
    # ensure Vertex AI is initialized, typically with vertexai.init()
    # This client assumes that initialization is handled elsewhere or not needed for these specific SDK calls
    # If agent_engine_manager.py functions require explicit vertexai.init(),
    # you might need to add it here or ensure it's called before using the client.
    main()