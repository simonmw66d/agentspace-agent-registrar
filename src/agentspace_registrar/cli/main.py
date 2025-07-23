"""
Main CLI entry point for AgentSpace Registrar.
"""
import typer
from typing import Optional

from .commands import registry, engine, auth

# Create the main app
app = typer.Typer(
    name="agentspace-registrar",
    help="Manage agents in Agentspace Agent Gallery and Agent Engine",
    add_completion=False,
)

# Add subcommand groups
app.add_typer(
    registry.app, 
    name="registry", 
    help="Agent Registry operations (Agentspace Agent Gallery)"
)
app.add_typer(
    engine.app, 
    name="engine", 
    help="Agent Engine operations (Vertex AI Agent Engine)"
)
app.add_typer(
    auth.app, 
    name="auth", 
    help="Authorization operations"
)

# Add a version command
def version_callback(value: bool):
    if value:
        typer.echo("AgentSpace Registrar v0.1.0")
        raise typer.Exit()

app.callback()(
    lambda version: version_callback(version)
)

if __name__ == "__main__":
    app() 