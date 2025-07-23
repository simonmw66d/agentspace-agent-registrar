"""
Configuration manager for AgentSpace Registrar.
Handles loading configuration from files and resolving parameters with proper precedence.
"""
import json
import os
import logging
from typing import Any, Dict, Optional
from pathlib import Path

from .models import GlobalConfig

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages configuration loading and parameter resolution with precedence:
    1. Command-line arguments
    2. Configuration file
    3. Environment variables
    4. Default values
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to configuration file (defaults to config.json)
        """
        self.config_file = config_file or "config.json"
        self._config: Optional[GlobalConfig] = None
        self._cli_args: Dict[str, Any] = {}
    
    def load_config(self) -> GlobalConfig:
        """Load configuration from file."""
        if self._config is not None:
            return self._config
            
        config_path = Path(self.config_file).expanduser()
        
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config_data = json.load(f)
                self._config = GlobalConfig(**config_data)
                logger.debug(f"Loaded configuration from {config_path}")
            except json.JSONDecodeError as e:
                logger.warning(f"Could not decode JSON from config file {config_path}: {e}")
                self._config = GlobalConfig()
            except Exception as e:
                logger.warning(f"Error loading config file {config_path}: {e}")
                self._config = GlobalConfig()
        else:
            logger.debug(f"Config file {config_path} not found, using defaults")
            self._config = GlobalConfig()
        
        return self._config
    
    def set_cli_args(self, args: Dict[str, Any]) -> None:
        """Set command-line arguments for parameter resolution."""
        self._cli_args = args
    
    def get_parameter(
        self, 
        name: str, 
        prompt: Optional[str] = None, 
        required: bool = False, 
        default: Any = None
    ) -> Any:
        """
        Get a parameter value with defined precedence:
        1. Command-line arguments
        2. Configuration file
        3. Environment variables
        4. User prompt (if specified)
        5. Default value
        
        Args:
            name: Parameter name
            prompt: Optional prompt for user input
            required: Whether the parameter is required
            default: Default value if not found elsewhere
            
        Returns:
            Parameter value
            
        Raises:
            ValueError: If required parameter is not found
        """
        config = self.load_config()
        
        # 1. Command-line arguments
        if name in self._cli_args and self._cli_args[name] is not None:
            value = self._cli_args[name]
            logger.debug(f"Parameter '{name}' from CLI: '{value}'")
            return value
        
        # 2. Configuration file
        if hasattr(config, name):
            value = getattr(config, name)
            if value is not None:
                logger.debug(f"Parameter '{name}' from config file: '{value}'")
                return value
        
        # 3. Environment variables
        env_name = f"AGENTSPACE_{name.upper()}"
        if env_name in os.environ:
            value = os.environ[env_name]
            logger.debug(f"Parameter '{name}' from environment: '{value}'")
            return value
        
        # 4. User prompt
        if prompt:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                logger.debug(f"Parameter '{name}' from prompt: '{user_input}'")
                return user_input
            elif default is None and required:
                raise ValueError(f"Parameter '{name}' is required but was not provided via prompt.")
        
        # 5. Default value
        if default is not None:
            logger.debug(f"Parameter '{name}' from default: '{default}'")
            return default
        
        if required:
            raise ValueError(f"Parameter '{name}' is required but not found via CLI, config, or prompt.")
        
        return None
    
    def get_agent_registry_config(self) -> Dict[str, Any]:
        """Get configuration for Agent Registry operations."""
        return {
            "project_id": self.get_parameter("project_id", required=True),
            "app_id": self.get_parameter("app_id", required=True),
            "api_location": self.get_parameter("api_location", default="global"),
            "re_location": self.get_parameter("re_location", default="global"),
        }
    
    def get_agent_engine_config(self) -> Dict[str, Any]:
        """Get configuration for Agent Engine operations."""
        return {
            "project_id": self.get_parameter("project_id", required=True),
            "location": self.get_parameter("location", default="us-central1"),
        }
    
    def get_agent_config(self) -> Dict[str, Any]:
        """Get configuration for agent operations."""
        return {
            "display_name": self.get_parameter("ars_display_name", required=True),
            "description": self.get_parameter("description", required=True),
            "tool_description": self.get_parameter("tool_description", required=True),
            "adk_deployment_id": self.get_parameter("adk_deployment_id", required=True),
            "auth_id": self.get_parameter("auth_id"),
            "icon_uri": self.get_parameter("icon_uri"),
        } 