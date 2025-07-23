"""
Custom exceptions for AgentSpace Registrar.
"""


class AgentRegistrarError(Exception):
    """Base exception for all AgentRegistrar errors."""
    pass


class ConfigurationError(AgentRegistrarError):
    """Configuration-related errors."""
    pass


class AuthenticationError(AgentRegistrarError):
    """Authentication-related errors."""
    pass


class ServiceError(AgentRegistrarError):
    """Service operation errors."""
    pass


class ValidationError(AgentRegistrarError):
    """Input validation errors."""
    pass


class InitializationError(AgentRegistrarError):
    """SDK initialization errors."""
    pass 