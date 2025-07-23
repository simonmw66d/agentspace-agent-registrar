"""
Output formatting utilities for AgentSpace Registrar.
"""
import json
from typing import Any, Dict, List


def format_json(data: Any, indent: int = 2) -> str:
    """
    Format data as JSON string.
    
    Args:
        data: Data to format
        indent: JSON indentation level
        
    Returns:
        Formatted JSON string
    """
    if isinstance(data, str):
        # If it's already a JSON string, parse and re-format
        try:
            parsed = json.loads(data)
            return json.dumps(parsed, indent=indent)
        except json.JSONDecodeError:
            # If it's not valid JSON, return as is
            return data
    
    return json.dumps(data, indent=indent)


def print_json(data: Any, indent: int = 2) -> None:
    """
    Print data as formatted JSON.
    
    Args:
        data: Data to print
        indent: JSON indentation level
    """
    print(format_json(data, indent))


def format_agent_list(agents: List[Dict[str, Any]]) -> str:
    """
    Format a list of agents for display.
    
    Args:
        agents: List of agent dictionaries
        
    Returns:
        Formatted string representation
    """
    if not agents:
        return "No agents found."
    
    lines = []
    for i, agent in enumerate(agents, 1):
        lines.append(f"{i}. {agent.get('display_name', 'Unknown')}")
        lines.append(f"   ID: {agent.get('name', 'Unknown')}")
        if 'description' in agent:
            lines.append(f"   Description: {agent['description']}")
        lines.append("")
    
    return "\n".join(lines)


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"❌ {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"⚠️  {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"ℹ️  {message}") 