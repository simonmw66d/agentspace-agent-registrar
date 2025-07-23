"""
Configuration models for AgentSpace Registrar.
"""
from pydantic import BaseModel, Field
from typing import Optional


class AgentRegistryConfig(BaseModel):
    """Configuration for Agent Registry operations."""
    project_id: str = Field(..., description="Google Cloud Project ID")
    app_id: str = Field(..., description="App ID for the Discovery Engine")
    api_location: str = Field(default="global", description="API location for Discovery Engine service")
    re_location: str = Field(default="global", description="Location of Reasoning Engine and Authorizations")


class AgentEngineConfig(BaseModel):
    """Configuration for Agent Engine operations."""
    project_id: str = Field(..., description="Google Cloud Project ID")
    location: str = Field(default="us-central1", description="Google Cloud Location/Region for Vertex AI")


class AgentConfig(BaseModel):
    """Configuration for individual agent operations."""
    display_name: str = Field(..., description="Display name of the agent")
    description: str = Field(..., description="Description of the agent")
    tool_description: str = Field(..., description="Tool description for the agent")
    adk_deployment_id: str = Field(..., description="Reasoning Engine ID from agent deployment")
    auth_id: Optional[str] = Field(default=None, description="Authorization ID (optional)")
    icon_uri: Optional[str] = Field(default=None, description="Icon URI for the agent")


class AuthorizationConfig(BaseModel):
    """Configuration for authorization operations."""
    project_id: str = Field(..., description="Google Cloud Project ID")
    location: str = Field(default="us", description="Location for authorization operations")
    authorization_id: str = Field(..., description="Authorization ID")
    scopes: list[str] = Field(default=["email"], description="OAuth scopes")


class GlobalConfig(BaseModel):
    """Global configuration that can be loaded from config file."""
    # Agent Registry fields
    project_id: Optional[str] = Field(default=None, description="Google Cloud Project ID")
    app_id: Optional[str] = Field(default=None, description="App ID for the Discovery Engine")
    ars_display_name: Optional[str] = Field(default=None, description="Agent display name for registry")
    description: Optional[str] = Field(default=None, description="Agent description for registry")
    tool_description: Optional[str] = Field(default=None, description="Tool description for registry")
    adk_deployment_id: Optional[str] = Field(default=None, description="Reasoning Engine ID from agent deployment")
    auth_id: Optional[str] = Field(default=None, description="OAuth authorization ID")
    icon_uri: Optional[str] = Field(default=None, description="Icon URI for the agent")
    api_location: str = Field(default="global", description="API location for Discovery Engine service")
    re_location: str = Field(default="global", description="Location of Reasoning Engine and Authorizations")
    
    # Agent Engine fields
    location: Optional[str] = Field(default=None, description="Google Cloud Location/Region for Vertex AI")
    re_resource_name: Optional[str] = Field(default=None, description="Full resource name of deployed agent")
    re_resource_id: Optional[str] = Field(default=None, description="Resource ID of deployed agent")
    re_display_name: Optional[str] = Field(default=None, description="Display name of deployed agent")
    
    # Agent Registry specific
    agent_id: Optional[str] = Field(default=None, description="Agent ID assigned by Agent Registry Service") 