import argparse
import agent_engine_manager
import os
import json
import logging
from dotenv import load_dotenv

# Configure logging for the client
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_parameter(name, args, prompt=None, required=False, default=None):
    """
    Retrieves a parameter value.
    Checks command-line arguments first, then environment variables (if applicable for project_id),
    then prompts the user if necessary.
    """
    value = getattr(args, name, None)
    if value is not None:
        return value

    # For project_id, also check environment variable GOOGLE_CLOUD_PROJECT
    if name == "project_id":
        env_value = os.getenv("GOOGLE_CLOUD_PROJECT")
        if env_value:
            return env_value
    
    if prompt:
        user_input = input(f"{prompt}: ")
        if user_input:
            return user_input
    
    if required and not value and not default:
        raise ValueError(f"Parameter '{name}' is required.")
    return default if default is not None else None

def main():
    # Load environment variables from .env file if it exists
    load_dotenv()

    parser = argparse.ArgumentParser(description="Agent Engine Manager Client")
    parser.add_argument(
        "action", nargs='?', # Make action optional to allow prompting
        choices=["list_deployed_agents", "undeploy_agent", "get_deployed_agent", "list_deployed_agents_by_name"],
        help="Action to perform: \n"
             "  list_deployed_agents: List all deployed agents.\n"
             "  undeploy_agent: Undeploy an agent by resource name.\n"
             "  get_deployed_agent: Get a deployed agent by resource ID.\n"
             "  list_deployed_agents_by_name: List deployed agents by display name."
    )
    parser.add_argument(
        "--resource_name",
        help="Resource name of the agent (e.g., projects/PROJECT_ID/locations/LOCATION/agents/AGENT_ID). Required for 'undeploy_agent'."
    )
    parser.add_argument(
        "--resource_id",
        help="Resource ID of the agent. Required for 'get_deployed_agent'."
    )
    parser.add_argument(
        "--display_name",
        help="Display name of the agent. Required for 'list_by_name'."
    )
    parser.add_argument(
        "--project_id",
        help="Google Cloud Project ID. Can also be set via GOOGLE_CLOUD_PROJECT env var or .env file."
    )
    parser.add_argument(
        "--location",
        help="Google Cloud Location/Region for Vertex AI. Defaults to None (SDK will use its default, often 'us-central1')."
    )

    args = parser.parse_args()

    action = args.action
    if not action:
        action = input(
            "Enter action to perform (list_deployed_agents, undeploy_agent, get_deployed_agent, list_deployed_agents_by_name): "
        ).strip().lower()
        if action not in ["list_deployed_agents", "undeploy_agent", "get_deployed_agent", "list_deployed_agents_by_name"]:
            logger.error(f"Invalid action: {action}")
            parser.print_help()
            return

    try:
        # Get Project ID: CLI > Environment Variable (from .env or shell) > Prompt
        project_id = get_parameter(
            "project_id", args,
            prompt="Enter Google Cloud Project ID",
            required=True
        )
        
        location = get_parameter(
            "location", args,
            prompt="Enter Google Cloud Location (optional, press Enter for default)",
            required=False,
            default=None # Pass None if not provided, so vertexai.init uses its default
        )

        # Initialize Vertex AI in the manager module
        agent_engine_manager.initialize_vertex_ai(project_id, location)
        logger.info(f"Client proceeding with action: {action}")


        if action == "list_deployed_agents":
            result = agent_engine_manager.list_agents()
            print(result)
        elif action == "undeploy_agent":
            resource_name = get_parameter(
                "resource_name", args, 
                prompt="Enter resource name of the agent to undeploy (e.g., projects/PROJECT_ID/locations/LOCATION/agents/AGENT_ID)",
                required=True
            )
            # No need for the 'if not resource_name' check here as get_parameter handles 'required'
            
            confirmation = input(f"Are you sure you want to undeploy agent with resource name '{resource_name}'? (yes/no): ")
            if confirmation.lower() == "yes":
                result = agent_engine_manager.delete_agent(resource_name)
                print(result)
            else:
                print("Undeployment cancelled.")

        elif action == "get_deployed_agent":
            resource_id = get_parameter(
                "resource_id", args, 
                prompt="Enter resource ID of the agent to get",
                required=True
            )
            result = agent_engine_manager.get_agent(resource_id)
            print(result)

        elif action == "list_deployed_agents_by_name":
            display_name = get_parameter(
                "display_name", args, 
                prompt="Enter display name of the agent to list",
                required=True
            )
            result = agent_engine_manager.list_agents_by_display_name(display_name)
            print(result)
        # No 'else' needed here as action is validated earlier

    except ValueError as ve: # Catch errors from get_parameter if required field is missing
        logger.error(f"Configuration error: {ve}")
    except RuntimeError as re: # Catch errors from _ensure_vertex_ai_initialized
        logger.error(f"SDK Initialization error: {re}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    # The client now handles calling agent_engine_manager.initialize_vertex_ai()
    # with the project_id and location obtained from CLI args, .env, or user prompt.
    main()