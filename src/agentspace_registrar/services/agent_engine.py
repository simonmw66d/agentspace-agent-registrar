"""
Agent Engine service for managing agents in Vertex AI Agent Engine.
Refactored from the original agent_engine_manager.py with better error handling.
"""
import json
import logging
from typing import Dict, Any, List, Optional

import vertexai
from vertexai import agent_engines

from ..exceptions import ServiceError, InitializationError

logger = logging.getLogger(__name__)


class AgentEngineService:
    """Service for managing agents in Vertex AI Agent Engine."""
    
    def __init__(self):
        self._initialized = False
        self._project_id: Optional[str] = None
        self._location: Optional[str] = None
    
    def initialize(self, project_id: str, location: Optional[str] = None) -> None:
        """
        Initialize the Vertex AI SDK.
        
        Args:
            project_id: Google Cloud Project ID
            location: Google Cloud Location/Region (optional)
            
        Raises:
            InitializationError: If initialization fails
        """
        if not project_id:
            raise InitializationError("Project ID cannot be None or empty")
        
        try:
            vertexai.init(project=project_id, location=location)
            self._initialized = True
            self._project_id = project_id
            self._location = location
            logger.info(f"Vertex AI initialized successfully for project: {project_id}" + (f" and location: {location}" if location else ""))
        except Exception as e:
            logger.error(f"Error initializing Vertex AI for project {project_id}: {e}")
            self._initialized = False
            raise InitializationError(f"Failed to initialize Vertex AI: {e}")
    
    def _ensure_initialized(self) -> None:
        """Ensure Vertex AI has been initialized."""
        if not self._initialized:
            raise InitializationError(
                "Vertex AI SDK has not been initialized. "
                "Please call initialize(project_id, [location]) first."
            )
    
    def list_agents(self) -> Dict[str, Any]:
        """
        List all agents in the Agent Engine.
        
        Returns:
            List of agents with their details
            
        Raises:
            ServiceError: If the operation fails
            InitializationError: If not initialized
        """
        self._ensure_initialized()
        
        try:
            agents_list = []
            for agent in agent_engines.list():
                agents_list.append({
                    "name": agent.name,
                    "display_name": agent.display_name,
                    "resource_name": agent.resource_name,
                    "create_time": str(agent.create_time)
                })
            
            logger.info(f"Found {len(agents_list)} agents")
            return {"agents": agents_list}
        except Exception as e:
            logger.error(f"Error listing agents: {e}")
            raise ServiceError(f"Failed to list agents: {e}")
    
    def get_agent(self, resource_id: str) -> Dict[str, Any]:
        """
        Get a specific agent by resource ID.
        
        Args:
            resource_id: Resource ID of the agent to retrieve
            
        Returns:
            Agent details
            
        Raises:
            ServiceError: If the operation fails
            InitializationError: If not initialized
        """
        self._ensure_initialized()
        
        try:
            agent = agent_engines.get(resource_id)
            agent_data = {
                "name": agent.name,
                "display_name": agent.display_name,
                "resource_name": agent.resource_name,
                "create_time": str(agent.create_time)
            }
            
            logger.info(f"Successfully retrieved agent: {resource_id}")
            return agent_data
        except Exception as e:
            logger.error(f"Error getting agent {resource_id}: {e}")
            raise ServiceError(f"Failed to get agent {resource_id}: {e}")
    
    def list_agents_by_display_name(self, display_name: str) -> Dict[str, Any]:
        """
        List agents by display name.
        
        Args:
            display_name: Display name to filter by
            
        Returns:
            List of matching agents
            
        Raises:
            ServiceError: If the operation fails
            InitializationError: If not initialized
        """
        self._ensure_initialized()
        
        try:
            agents_list = []
            filter_expr = f'display_name="{display_name}"'
            
            for agent in agent_engines.list(filter=filter_expr):
                agents_list.append({
                    "name": agent.name,
                    "display_name": agent.display_name,
                    "resource_name": agent.resource_name,
                    "create_time": str(agent.create_time)
                })
            
            logger.info(f"Found {len(agents_list)} agents with display name: {display_name}")
            return {"agents": agents_list}
        except Exception as e:
            logger.error(f"Error listing agents by display name {display_name}: {e}")
            raise ServiceError(f"Failed to list agents by display name {display_name}: {e}")
    
    def delete_agent(self, resource_name: str) -> Dict[str, Any]:
        """
        Delete an agent from the Agent Engine.
        
        Args:
            resource_name: Full resource name of the agent to delete
            
        Returns:
            Deletion result
            
        Raises:
            ServiceError: If the operation fails
            InitializationError: If not initialized
        """
        self._ensure_initialized()
        
        try:
            agent_engines.delete(resource_name)
            logger.info(f"Successfully deleted agent: {resource_name}")
            return {"message": f"Agent with resource name {resource_name} deleted successfully"}
        except Exception as e:
            logger.error(f"Error deleting agent {resource_name}: {e}")
            raise ServiceError(f"Failed to delete agent {resource_name}: {e}") 