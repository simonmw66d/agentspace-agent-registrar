"""
Agent Engine commands for managing agents in Vertex AI Agent Engine.
"""
import typer
from typing import Optional

from ..base import EngineCommand
from ...config.manager import ConfigManager
from ...utils.output import print_success


# Create the engine app
app = typer.Typer(
    name="engine",
    help="Agent Engine operations (Vertex AI Agent Engine)",
    add_completion=False,
)


class ListAgentsCommand(EngineCommand):
    """List all agents in the Agent Engine."""
    
    def execute(self, **kwargs) -> dict:
        config = self.get_engine_config()
        
        from ...services.agent_engine import AgentEngineService
        
        service = AgentEngineService()
        service.initialize(**config)
        return service.list_agents()


class GetAgentCommand(EngineCommand):
    """Get a specific agent by resource ID."""
    
    def execute(self, **kwargs) -> dict:
        resource_id = kwargs.get('resource_id')
        if not resource_id:
            raise ValueError("resource_id is required")
            
        config = self.get_engine_config()
        
        from ...services.agent_engine import AgentEngineService
        
        service = AgentEngineService()
        service.initialize(**config)
        return service.get_agent(resource_id=resource_id)


class ListAgentsByNameCommand(EngineCommand):
    """List agents by display name."""
    
    def execute(self, **kwargs) -> dict:
        display_name = kwargs.get('display_name')
        if not display_name:
            raise ValueError("display_name is required")
            
        config = self.get_engine_config()
        
        from ...services.agent_engine import AgentEngineService
        
        service = AgentEngineService()
        service.initialize(**config)
        return service.list_agents_by_display_name(display_name=display_name)


class DeleteAgentCommand(EngineCommand):
    """Delete an agent from the Agent Engine."""
    
    def execute(self, **kwargs) -> dict:
        resource_name = kwargs.get('resource_name')
        if not resource_name:
            raise ValueError("resource_name is required")
            
        config = self.get_engine_config()
        
        from ...services.agent_engine import AgentEngineService
        
        service = AgentEngineService()
        service.initialize(**config)
        return service.delete_agent(resource_name=resource_name)


# Command implementations
@app.command("list")
def list_agents(
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us-central1", "--location", help="Google Cloud Location/Region"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """List all agents in the Agent Engine."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = ListAgentsCommand(config_manager)
    command.run()


@app.command("get")
def get_agent(
    resource_id: str = typer.Argument(..., help="Resource ID of the agent to retrieve"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us-central1", "--location", help="Google Cloud Location/Region"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """Get a specific agent by resource ID."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = GetAgentCommand(config_manager)
    command.run(resource_id=resource_id)


@app.command("list-by-name")
def list_agents_by_name(
    display_name: str = typer.Argument(..., help="Display name to search for"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us-central1", "--location", help="Google Cloud Location/Region"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """List agents by display name."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = ListAgentsByNameCommand(config_manager)
    command.run(display_name=display_name)


@app.command("delete")
def delete_agent(
    resource_name: str = typer.Argument(..., help="Full resource name of the agent to delete"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us-central1", "--location", help="Google Cloud Location/Region"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
    force: bool = typer.Option(False, "--force", help="Skip confirmation prompt"),
):
    """Delete an agent from the Agent Engine."""
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete agent '{resource_name}'?")
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()
    
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = DeleteAgentCommand(config_manager)
    command.run(resource_name=resource_name)
    print_success(f"Agent '{resource_name}' deleted successfully.") 