"""
Authentication utilities for AgentSpace Registrar.
"""
import logging
import google.auth
import google.auth.transport.requests

from ..exceptions import AuthenticationError

logger = logging.getLogger(__name__)

# Scopes define the level of access you are requesting.
# For this example, we are using the default cloud-platform scope.
# You may need to specify more granular scopes depending on your needs.
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']


def get_access_token():
    """
    Gets the access token from the environment.
    
    Returns:
        str: Access token for API authentication
        
    Raises:
        AuthenticationError: If authentication fails
    """
    try:
        # google.auth.default() automatically finds the credentials
        # from the environment (e.g., a service account key).
        credentials, project_id = google.auth.default(scopes=SCOPES)

        # Refresh the credentials to get an access token.
        # Provide a transport object for refreshing.
        credentials.refresh(google.auth.transport.requests.Request())

        return credentials.token
    except Exception as e:
        logger.error(f"An error occurred in get_access_token: {e}")
        import traceback
        traceback.print_exc()  # This will print the full stack trace
        raise AuthenticationError(f"Failed to obtain access token: {e}") 