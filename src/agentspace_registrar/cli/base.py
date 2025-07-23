"""
Base classes for CLI commands.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import typer

from ..config.manager import ConfigManager
from ..exceptions import AgentRegistrarError, ConfigurationError
from ..utils.output import print_error, print_json


class BaseCommand(ABC):
    """Base class for all CLI commands."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the command.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the command.
        
        Args:
            **kwargs: Command-specific arguments
            
        Returns:
            Command result
        """
        pass
    
    def run(self, **kwargs) -> None:
        """
        Run the command with error handling and output formatting.
        
        Args:
            **kwargs: Command-specific arguments
        """
        try:
            result = self.execute(**kwargs)
            if result:
                print_json(result)
        except ConfigurationError as e:
            print_error(f"Configuration error: {e}")
            raise typer.Exit(1)
        except AgentRegistrarError as e:
            print_error(f"Operation failed: {e}")
            raise typer.Exit(1)
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            raise typer.Exit(1)


class RegistryCommand(BaseCommand):
    """Base class for Agent Registry commands."""
    
    def get_registry_config(self) -> Dict[str, Any]:
        """Get Agent Registry configuration."""
        return self.config_manager.get_agent_registry_config()


class EngineCommand(BaseCommand):
    """Base class for Agent Engine commands."""
    
    def get_engine_config(self) -> Dict[str, Any]:
        """Get Agent Engine configuration."""
        return self.config_manager.get_agent_engine_config()


class AuthCommand(BaseCommand):
    """Base class for Authorization commands."""
    
    def get_auth_config(self) -> Dict[str, Any]:
        """Get Authorization configuration."""
        return {
            "project_id": self.config_manager.get_parameter("project_id", required=True),
            "location": self.config_manager.get_parameter("location", default="us"),
        } 