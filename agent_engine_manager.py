import vertexai
from vertexai import agent_engines
import json

def list_agents():
    """
    Lists all agents in the Agent Engine.

    Returns:
        str: A JSON string representing a list of agents, each with name, display_name, resource_name, and create_time.
    """
    agents_list = []
    for agent in agent_engines.list():
        agents_list.append({
            "name": agent.name,
            "display_name": agent.display_name,
            "resource_name": agent.resource_name,
            "create_time": str(agent.create_time)
        })
    return json.dumps(agents_list, indent=2)


def delete_agent(resource_name):
    """
    Deletes an agent from the Agent Engine by its resource name.

    Args:
        resource_name (str): The resource name of the agent to delete.

    Returns:
        str: A success message indicating the agent was deleted.
    """
    agent_engines.delete(resource_name)
    return f"Agent with resource name {resource_name} deleted successfully."


def get_agent(resource_id):
    """Retrieves an agent from the Agent Engine by its resource ID."""
    # Assuming this is the correct method to retrieve by ID
    agent = agent_engines.get(resource_id)
    return json.dumps({
        "name": agent.name,
        "display_name": agent.display_name,
        "resource_name": agent.resource_name,
        "create_time": str(agent.create_time)
    }, indent=2)
    

def list_agents_by_display_name(display_name):
    """
    Lists agents in the Agent Engine that match a given display name.

    Args:
        display_name (str): The display name to filter agents by.

    Returns:
        str: A JSON string representing a list of agents matching the display name.
    """
    agents_list = []
    for agent in agent_engines.list(filter=f'display_name="{display_name}"'):
        agents_list.append({
            "name": agent.name,
            "display_name": agent.display_name,
            "resource_name": agent.resource_name,
            "create_time": str(agent.create_time)
        })
    return json.dumps(agents_list, indent=2)
    
