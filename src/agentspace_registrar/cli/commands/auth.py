"""
Authorization commands for managing OAuth authorizations.
"""
import typer
from typing import Optional, List

from ..base import AuthCommand
from ...config.manager import ConfigManager
from ...utils.output import print_success


# Create the auth app
app = typer.Typer(
    name="auth",
    help="Authorization operations",
    add_completion=False,
)


class CreateAuthorizationCommand(AuthCommand):
    """Create a new authorization."""
    
    def execute(self, **kwargs) -> dict:
        authorization_id = kwargs.get('authorization_id')
        scopes = kwargs.get('scopes', ['email'])
        
        config = self.get_auth_config()
        
        from ...services.authorization import AuthorizationService
        
        service = AuthorizationService()
        return service.create_authorization(
            scopes=scopes,
            authorization_id=authorization_id,
            **config
        )


class ListAuthorizationsCommand(AuthCommand):
    """List all authorizations."""
    
    def execute(self, **kwargs) -> dict:
        config = self.get_auth_config()
        
        from ...services.authorization import AuthorizationService
        
        service = AuthorizationService()
        return service.list_authorizations(**config)


class DeleteAuthorizationCommand(AuthCommand):
    """Delete an authorization."""
    
    def execute(self, **kwargs) -> dict:
        authorization_id = kwargs.get('authorization_id')
        
        if not authorization_id:
            raise ValueError("authorization_id is required")
            
        config = self.get_auth_config()
        
        from ...services.authorization import AuthorizationService
        
        service = AuthorizationService()
        return service.delete_authorization(
            authorization_id=authorization_id,
            **config
        )


class RefreshAuthorizationCommand(AuthCommand):
    """Refresh authorization by creating new one and deleting old one."""
    
    def execute(self, **kwargs) -> dict:
        old_auth_id = kwargs.get('old_auth_id')
        new_auth_id = kwargs.get('new_auth_id')
        scopes = kwargs.get('scopes', ['email'])
        
        if not old_auth_id:
            raise ValueError("old_auth_id is required")
            
        config = self.get_auth_config()
        
        from ...services.authorization import AuthorizationService
        
        service = AuthorizationService()
        
        # Create new authorization (new_auth_id is optional, will be auto-generated)
        create_result = service.create_authorization(
            scopes=scopes,
            authorization_id=new_auth_id,
            **config
        )
        
        # Extract the actual authorization ID from the create result
        actual_new_auth_id = new_auth_id
        if not actual_new_auth_id and create_result.get('name'):
            actual_new_auth_id = create_result['name'].split('/')[-1]
        
        # Delete old authorization
        delete_result = service.delete_authorization(
            authorization_id=old_auth_id,
            **config
        )
        
        return {
            "created": create_result,
            "deleted": delete_result,
            "message": f"Authorization refreshed: {old_auth_id} -> {actual_new_auth_id}"
        }


# Command implementations
@app.command("create")
def create_authorization(
    authorization_id: Optional[str] = typer.Argument(None, help="Authorization ID to create (optional, will generate UUID4 if not provided)"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us", "--location", help="Location for authorization"),
    scopes: List[str] = typer.Option(["email"], "--scopes", help="OAuth scopes"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """Create a new authorization."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = CreateAuthorizationCommand(config_manager)
    
    # Execute the command and get the result
    try:
        result = command.execute(authorization_id=authorization_id, scopes=scopes)
        
        # Extract the authorization ID from the result or use the provided one
        created_auth_id = authorization_id
        if not created_auth_id and result.get('name'):
            # Extract ID from the name field in the response
            created_auth_id = result['name'].split('/')[-1]
        
        # Print the result and success message
        from ...utils.output import print_json
        print_json(result)
        print_success(f"Authorization '{created_auth_id}' created successfully.")
        
    except Exception as e:
        from ...utils.output import print_error
        print_error(f"Failed to create authorization: {e}")
        raise typer.Exit(1)


@app.command("list")
def list_authorizations(
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us", "--location", help="Location for authorization"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """List all authorizations."""
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = ListAuthorizationsCommand(config_manager)
    command.run()


@app.command("delete")
def delete_authorization(
    authorization_id: str = typer.Argument(..., help="Authorization ID to delete"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us", "--location", help="Location for authorization"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
    force: bool = typer.Option(False, "--force", help="Skip confirmation prompt"),
):
    """Delete an authorization."""
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete authorization '{authorization_id}'?")
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()
    
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = DeleteAuthorizationCommand(config_manager)
    command.run(authorization_id=authorization_id)
    print_success(f"Authorization '{authorization_id}' deleted successfully.")


@app.command("refresh")
def refresh_authorization(
    old_auth_id: str = typer.Argument(..., help="Old authorization ID to replace"),
    new_auth_id: Optional[str] = typer.Option(None, "--new-auth-id", help="New authorization ID (auto-generated if not provided)"),
    project_id: Optional[str] = typer.Option(None, "--project-id", help="Google Cloud Project ID"),
    location: str = typer.Option("us", "--location", help="Location for authorization"),
    scopes: List[str] = typer.Option(["email"], "--scopes", help="OAuth scopes"),
    config_file: Optional[str] = typer.Option("config.json", "--config", help="Configuration file path"),
):
    """Refresh authorization by creating new one and deleting old one."""
    if not new_auth_id:
        typer.echo("No new authorization ID provided. Will auto-generate UUID4.")
    
    config_manager = ConfigManager(config_file)
    config_manager.set_cli_args(locals())
    
    command = RefreshAuthorizationCommand(config_manager)
    command.run(
        old_auth_id=old_auth_id,
        new_auth_id=new_auth_id,
        scopes=scopes
    ) 