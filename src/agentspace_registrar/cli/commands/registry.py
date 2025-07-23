"""
Agent Registry commands for managing agents in Agentspace Agent Gallery.
"""
import typer
from typing import Optional

from ..base import RegistryCommand
from ...config.manager import ConfigManager
from ...utils.output import print_success, print_warning

# Create the registry app
app = typer.Typer(
    name="registry",
    help="Agent Registry operations (Agentspace Agent Gallery)",
    add_completion=False,
)


class CreateAgentCommand(RegistryCommand):
    """Create a new agent in the registry."""
    
    def execute(self, **kwargs) -> dict:
        config = self.get_registry_config()
        agent_config = self.config_manager.get_agent_config()
        
        # Import here to avoid circular imports
        from ...services.agent_registry import AgentRegistryService
        
        service = AgentRegistryService()
        return service.create_agent(**config, **agent_config)


class ListAgentsCommand(RegistryCommand):
    """List all agents in the registry."""
    
    def execute(self, **kwargs) -> dict:
        config = self.get_registry_config()
        
        from ...services.agent_registry import AgentRegistryService
        
        service = AgentRegistryService()
        return service.list_agents(**config)


class GetAgentCommand(RegistryCommand):
    """Get a specific agent by ID."""
    
    def execute(self, **kwargs) -> dict:
        agent_id = kwargs.get('agent_id')
        if not agent_id:
            raise ValueError("agent_id is required")
            
        config = self.get_registry_config()
        
        from ...services.agent_registry import AgentRegistryService
        
        service = AgentRegistryService()
        return service.get_agent(agent_id=agent_id, **config)


class UpdateAgentCommand(RegistryCommand):
    """Update an existing agent."""
    
    def execute(self, **kwargs) -> dict:
        agent_id = kwargs.get('agent_id')
        if not agent_id:
            raise ValueError("agent_id is required")
            
        config = self.get_registry_config()
        agent_config = self.config_manager.get_agent_config()
        
        from ...services.agent_registry import AgentRegistryService
        
        service = AgentRegistryService()
        return service.update_agent(agent_id=agent_id, **config, **agent_config)


class GetAgentByNameCommand(RegistryCommand):
    """Get agents by display name."""
    
    def execute(self, **kwargs) -> dict:
        display_name = kwargs.get('display_name')
        if not display_name:
            raise ValueError("display_name is required")
            
        config = self.get_registry_config()
        
        from ...services.agent_registry import AgentRegistryService
        
        service = AgentRegistryService()
        return service.get_agent_by_display_name(display_name=display_name, **config)


class DeleteAgentCommand(RegistryCommand):
    """Delete an agent from the registry."""
    
    def execute(self, **kwargs) -> dict:
        agent_id = kwargs.get('agent_id')
        if not agent_id:
            raise ValueError("agent_id is required")
            
        config = self.get_registry_config()
        
        from ...services.agent_registry import AgentRegistryService
        
        service = AgentRegistryService()
        return service.delete_agent(agent_id=agent_id, **config)


# Command implementations
@app.command("create")
def create_agent(
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    app_id: Optional[str] = typer.Option(None, "--app-id", help="App ID for the Discovery Engine"),
    display_name: Optional[str] = typer.Option(None, "--display-name", help="Agent display name"),
    description: Optional[str] = typer.Option(None, "--description", help="Agent description"),
    tool_description: Optional[str] = typer.Option(None, "--tool-description", help="Tool description"),
    adk_deployment_id: Optional[str] = typer.Option(None, "--adk-deployment-id", help="Reasoning Engine ID"),
    auth_id: Optional[str] = typer.Option(None, "--auth-id", help="Authorization ID"),
    icon_uri: Optional[str] = typer.Option(None, "--icon-uri", help="Icon URI for the agent"),
    api_location: str = typer.Option("global", "--api-location", help="API location"),
    re_location: str = typer.Option("global", "--re-location", help="Reasoning Engine location"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """Create a new agent in the Agent Registry."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = CreateAgentCommand(config_manager)
    command.run()


@app.command("list")
def list_agents(
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    app_id: Optional[str] = typer.Option(None, "--app-id", help="App ID for the Discovery Engine"),
    api_location: str = typer.Option("global", "--api-location", help="API location"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """List all agents in the Agent Registry."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = ListAgentsCommand(config_manager)
    command.run()


@app.command("get")
def get_agent(
    agent_id: str = typer.Argument(..., help="Agent ID to retrieve"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    app_id: Optional[str] = typer.Option(None, "--app-id", help="App ID for the Discovery Engine"),
    api_location: str = typer.Option("global", "--api-location", help="API location"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """Get a specific agent by ID."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = GetAgentCommand(config_manager)
    command.run(agent_id=agent_id)


@app.command("update")
def update_agent(
    agent_id: str = typer.Argument(..., help="Agent ID to update"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    app_id: Optional[str] = typer.Option(None, "--app-id", help="App ID for the Discovery Engine"),
    display_name: Optional[str] = typer.Option(None, "--display-name", help="New display name"),
    description: Optional[str] = typer.Option(None, "--description", help="New description"),
    tool_description: Optional[str] = typer.Option(None, "--tool-description", help="New tool description"),
    adk_deployment_id: Optional[str] = typer.Option(None, "--adk-deployment-id", help="New Reasoning Engine ID"),
    auth_id: Optional[str] = typer.Option(None, "--auth-id", help="New authorization ID"),
    icon_uri: Optional[str] = typer.Option(None, "--icon-uri", help="New icon URI"),
    api_location: str = typer.Option("global", "--api-location", help="API location"),
    re_location: str = typer.Option("global", "--re-location", help="Reasoning Engine location"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """Update an existing agent."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = UpdateAgentCommand(config_manager)
    command.run(agent_id=agent_id)


@app.command("get-by-name")
def get_agent_by_name(
    display_name: str = typer.Argument(..., help="Display name to search for"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    app_id: Optional[str] = typer.Option(None, "--app-id", help="App ID for the Discovery Engine"),
    api_location: str = typer.Option("global", "--api-location", help="API location"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """Get agents by display name."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = GetAgentByNameCommand(config_manager)
    command.run(display_name=display_name)


@app.command("delete")
def delete_agent(
    agent_id: str = typer.Argument(..., help="Agent ID to delete"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    app_id: Optional[str] = typer.Option(None, "--app-id", help="App ID for the Discovery Engine"),
    api_location: str = typer.Option("global", "--api-location", help="API location"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
    force: bool = typer.Option(False, "--force", help="Skip confirmation prompt"),
):
    """Delete an agent from the registry."""
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete agent '{agent_id}'?")
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()
    
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = DeleteAgentCommand(config_manager)
    command.run(agent_id=agent_id)
    print_success(f"Agent '{agent_id}' deleted successfully.") 