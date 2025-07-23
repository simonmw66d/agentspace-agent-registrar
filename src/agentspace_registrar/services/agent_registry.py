"""
Agent Registry service for managing agents in Agentspace Agent Gallery.
Uses httpx for HTTP requests instead of curl subprocess calls.
"""
import json
import logging
from typing import Dict, Any, Optional, List

import httpx

from ..utils.auth import get_access_token
from ..exceptions import ServiceError, AuthenticationError

logger = logging.getLogger(__name__)

# Constants for URL construction
BASE_API_URL = "https://{location_prefix}discoveryengine.googleapis.com/v1alpha"
DEFAULT_LOCATION = "global"
DEFAULT_COLLECTION = "default_collection"
DEFAULT_ASSISTANT = "default_assistant"


class AgentRegistryService:
    """Service for managing agents in the Agent Registry."""
    
    def __init__(self):
        self.client = httpx.Client(timeout=30.0)
    
    def __del__(self):
        """Clean up the HTTP client."""
        if hasattr(self, 'client'):
            self.client.close()
    
    def _build_url(self, project_id: str, app_id: str, agent_id: Optional[str] = None, api_location: str = DEFAULT_LOCATION) -> str:
        """Build the Discovery Engine API URL for agents."""
        location_prefix = ""
        if api_location != "global":
            location_prefix = api_location + "-"
        
        url = BASE_API_URL.format(location_prefix=location_prefix)
        base_path = f"{url}/projects/{project_id}/locations/{api_location}/collections/{DEFAULT_COLLECTION}/engines/{app_id}/assistants/{DEFAULT_ASSISTANT}/agents"
        
        if agent_id:
            return f"{base_path}/{agent_id}"
        return base_path
    
    def _get_headers(self, project_id: str) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        access_token = get_access_token()
        if not access_token:
            raise AuthenticationError("Failed to obtain access token")
        
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Goog-User-Project": project_id,
        }
    
    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and return appropriate result."""
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise ServiceError(f"HTTP error {e.response.status_code}: {e.response.text}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise ServiceError(f"Invalid JSON response: {e}")
    
    def create_agent(
        self,
        project_id: str,
        app_id: str,
        display_name: str,
        description: str,
        tool_description: str,
        adk_deployment_id: str,
        auth_id: Optional[str] = None,
        icon_uri: Optional[str] = None,
        re_location: str = "global",
        api_location: str = "global"
    ) -> Dict[str, Any]:
        """
        Create a new agent in the Agent Registry.
        
        Args:
            project_id: Google Cloud Project ID
            app_id: App ID for the Discovery Engine
            display_name: Display name of the agent
            description: Description of the agent
            tool_description: Tool description for the agent
            adk_deployment_id: Reasoning Engine ID
            auth_id: Authorization ID (optional)
            icon_uri: Icon URI for the agent (optional)
            re_location: Location of the Reasoning Engine
            api_location: API location for the Discovery Engine service
            
        Returns:
            Created agent data
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        url = self._build_url(project_id, app_id, api_location=api_location)
        headers = self._get_headers(project_id)
        
        # Prepare the request body
        data = {
            "displayName": display_name,
            "description": description,
            "adk_agent_definition": {
                "tool_settings": {
                    "tool_description": tool_description
                },
                "provisioned_reasoning_engine": {
                    "reasoning_engine": f"projects/{project_id}/locations/{re_location}/reasoningEngines/{adk_deployment_id}"
                },
                "authorizations": [f"projects/{project_id}/locations/{api_location}/authorizations/{auth_id}"] if auth_id else [],
            }
        }
        
        if icon_uri:
            data["icon"] = {"uri": icon_uri}
        
        logger.info(f"Creating agent: {display_name}")
        response = self.client.post(url, headers=headers, json=data)
        
        result = self._handle_response(response)
        logger.info(f"Successfully created agent: {result.get('name', 'unknown')}")
        return result
    
    def list_agents(self, project_id: str, app_id: str, api_location: str = "global") -> Dict[str, Any]:
        """
        List all agents in the Agent Registry.
        
        Args:
            project_id: Google Cloud Project ID
            app_id: App ID for the Discovery Engine
            api_location: API location for the Discovery Engine service
            
        Returns:
            List of agents
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        url = self._build_url(project_id, app_id, api_location=api_location)
        headers = self._get_headers(project_id)
        
        logger.info(f"Listing agents for app: {app_id}")
        response = self.client.get(url, headers=headers)
        
        result = self._handle_response(response)
        agents = result.get("agents", [])
        logger.info(f"Found {len(agents)} agents")
        return {"agents": agents}
    
    def get_agent(self, agent_id: str, project_id: str, app_id: str, api_location: str = "global") -> Dict[str, Any]:
        """
        Get a specific agent by ID.
        
        Args:
            agent_id: ID of the agent to retrieve
            project_id: Google Cloud Project ID
            app_id: App ID for the Discovery Engine
            api_location: API location for the Discovery Engine service
            
        Returns:
            Agent data
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        url = self._build_url(project_id, app_id, agent_id, api_location=api_location)
        headers = self._get_headers(project_id)
        
        logger.info(f"Getting agent: {agent_id}")
        response = self.client.get(url, headers=headers)
        
        result = self._handle_response(response)
        logger.info(f"Successfully retrieved agent: {agent_id}")
        return result
    
    def update_agent(
        self,
        agent_id: str,
        project_id: str,
        app_id: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        tool_description: Optional[str] = None,
        adk_deployment_id: Optional[str] = None,
        auth_id: Optional[str] = None,
        icon_uri: Optional[str] = None,
        re_location: str = "global",
        api_location: str = "global"
    ) -> Dict[str, Any]:
        """
        Update an existing agent.
        
        Args:
            agent_id: ID of the agent to update
            project_id: Google Cloud Project ID
            app_id: App ID for the Discovery Engine
            display_name: New display name (optional)
            description: New description (optional)
            tool_description: New tool description (optional)
            adk_deployment_id: New Reasoning Engine ID (optional)
            auth_id: New authorization ID (optional)
            icon_uri: New icon URI (optional)
            re_location: Location of the Reasoning Engine
            api_location: API location for the Discovery Engine service
            
        Returns:
            Updated agent data
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        url = self._build_url(project_id, app_id, agent_id, api_location=api_location)
        headers = self._get_headers(project_id)
        
        # Build update mask and data
        update_mask_parts: List[str] = []
        data: Dict[str, Any] = {}
        
        if display_name is not None:
            data["displayName"] = display_name
            update_mask_parts.append("displayName")
        
        if description is not None:
            data["description"] = description
            update_mask_parts.append("description")
        
        if tool_description is not None:
            data["adk_agent_definition.tool_settings.tool_description"] = tool_description
            update_mask_parts.append("adk_agent_definition.tool_settings.tool_description")
        
        if adk_deployment_id is not None:
            data["adk_agent_definition.provisioned_reasoning_engine.reasoning_engine"] = f"projects/{project_id}/locations/{re_location}/reasoningEngines/{adk_deployment_id}"
            update_mask_parts.append("adk_agent_definition.provisioned_reasoning_engine.reasoning_engine")
        
        if auth_id is not None:
            data["adk_agent_definition.authorizations"] = [f"projects/{project_id}/locations/{api_location}/authorizations/{auth_id}"]
            update_mask_parts.append("adk_agent_definition.authorizations")
        
        if icon_uri is not None:
            data["icon.uri"] = icon_uri
            update_mask_parts.append("icon.uri")
        
        if not update_mask_parts:
            raise ServiceError("No fields to update")
        
        # Add update mask to query parameters
        params = {"updateMask": ",".join(update_mask_parts)}
        
        logger.info(f"Updating agent: {agent_id}")
        response = self.client.patch(url, headers=headers, json=data, params=params)
        
        result = self._handle_response(response)
        logger.info(f"Successfully updated agent: {agent_id}")
        return result
    
    def get_agent_by_display_name(self, display_name: str, project_id: str, app_id: str, api_location: str = "global") -> Dict[str, Any]:
        """
        Get agents by display name.
        
        Args:
            display_name: Display name to search for
            project_id: Google Cloud Project ID
            app_id: App ID for the Discovery Engine
            api_location: API location for the Discovery Engine service
            
        Returns:
            List of matching agents
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        url = self._build_url(project_id, app_id, api_location=api_location)
        headers = self._get_headers(project_id)
        
        # Add filter parameter
        params = {"filter": f'displayName="{display_name}"'}
        
        logger.info(f"Searching for agents with display name: {display_name}")
        response = self.client.get(url, headers=headers, params=params)
        
        result = self._handle_response(response)
        agents = result.get("agents", [])
        logger.info(f"Found {len(agents)} agents with display name: {display_name}")
        return {"agents": agents}
    
    def delete_agent(self, agent_id: str, project_id: str, app_id: str, api_location: str = "global") -> Dict[str, Any]:
        """
        Delete an agent from the Agent Registry.
        
        Args:
            agent_id: ID of the agent to delete
            project_id: Google Cloud Project ID
            app_id: App ID for the Discovery Engine
            api_location: API location for the Discovery Engine service
            
        Returns:
            Deletion result
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        url = self._build_url(project_id, app_id, agent_id, api_location=api_location)
        headers = self._get_headers(project_id)
        
        logger.info(f"Deleting agent: {agent_id}")
        response = self.client.delete(url, headers=headers)
        
        # DELETE requests typically return 204 No Content
        if response.status_code == 204:
            logger.info(f"Successfully deleted agent: {agent_id}")
            return {"message": f"Agent {agent_id} deleted successfully"}
        else:
            result = self._handle_response(response)
            logger.info(f"Successfully deleted agent: {agent_id}")
            return result 