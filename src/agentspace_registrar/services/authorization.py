"""
Authorization service for managing OAuth authorizations.
Refactored from the original authorization_service.py with better error handling.
"""
import os
import urllib.parse
import logging
from typing import Dict, Any, List

import httpx
from dotenv import load_dotenv

from ..utils.auth import get_access_token
from ..exceptions import ServiceError, AuthenticationError

load_dotenv()
logger = logging.getLogger(__name__)


class AuthorizationService:
    """Service for managing OAuth authorizations."""
    
    def __init__(self):
        self.client = httpx.Client(timeout=30.0)
    
    def __del__(self):
        """Clean up the HTTP client."""
        if hasattr(self, 'client'):
            self.client.close()
    
    def _get_endpoint(self, location: str) -> str:
        """Get the appropriate endpoint for the location."""
        if location[:2] in ["us", "eu"]:
            return f"{location[:2]}-discoveryengine.googleapis.com"
        return "discoveryengine.googleapis.com"  # global
    
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
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise ServiceError(f"Unexpected error: {e}")
    
    def create_authorization(
        self, 
        project_id: str, 
        location: str, 
        authorization_id: str, 
        scopes: List[str]
    ) -> Dict[str, Any]:
        """
        Create a new authorization.
        
        Args:
            project_id: Google Cloud Project ID
            location: Location for authorization operations
            authorization_id: Authorization ID to create
            scopes: OAuth scopes
            
        Returns:
            Created authorization data
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        endpoint = self._get_endpoint(location)
        url = f"https://{endpoint}/v1alpha/projects/{project_id}/locations/{location}/authorizations"
        headers = self._get_headers(project_id)
        
        # Build query string for OAuth parameters
        query_string = urllib.parse.urlencode({
            "client_id": os.getenv("OAUTH_CLIENT_ID"),
            "scope": " ".join(scopes),
            "include_granted_scopes": "true",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
        })
        
        authorization_uri = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
        logger.debug(f"Authorization URI: {authorization_uri}")
        
        # Prepare request data
        data = {
            "name": f"projects/{project_id}/locations/{location}/authorizations/{authorization_id}",
            "serverSideOauth2": {
                "clientId": os.getenv("OAUTH_CLIENT_ID"),
                "clientSecret": os.getenv("OAUTH_CLIENT_SECRET"),
                "authorizationUri": authorization_uri,
                "tokenUri": "https://oauth2.googleapis.com/token",
            },
        }
        
        # Add authorization ID to query parameters
        params = {"authorizationId": authorization_id}
        
        logger.info(f"Creating authorization: {authorization_id}")
        response = self.client.post(url, headers=headers, json=data, params=params)
        
        result = self._handle_response(response)
        logger.info(f"Successfully created authorization: {authorization_id}")
        return result
    
    def delete_authorization(self, project_id: str, location: str, authorization_id: str) -> Dict[str, Any]:
        """
        Delete an authorization.
        
        Args:
            project_id: Google Cloud Project ID
            location: Location for authorization operations
            authorization_id: Authorization ID to delete
            
        Returns:
            Deletion result
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        endpoint = self._get_endpoint(location)
        url = f"https://{endpoint}/v1alpha/projects/{project_id}/locations/{location}/authorizations/{authorization_id}"
        headers = self._get_headers(project_id)
        
        logger.info(f"Deleting authorization: {authorization_id}")
        response = self.client.delete(url, headers=headers)
        
        # DELETE requests typically return 204 No Content
        if response.status_code == 204:
            logger.info(f"Successfully deleted authorization: {authorization_id}")
            return {"message": f"Authorization {authorization_id} deleted successfully"}
        else:
            result = self._handle_response(response)
            logger.info(f"Successfully deleted authorization: {authorization_id}")
            return result
    
    def list_authorizations(self, project_id: str, location: str) -> Dict[str, Any]:
        """
        List all authorizations.
        
        Args:
            project_id: Google Cloud Project ID
            location: Location for authorization operations
            
        Returns:
            List of authorizations
            
        Raises:
            ServiceError: If the operation fails
            AuthenticationError: If authentication fails
        """
        endpoint = self._get_endpoint(location)
        url = f"https://{endpoint}/v1alpha/projects/{project_id}/locations/{location}/authorizations"
        headers = self._get_headers(project_id)
        
        logger.info(f"Listing authorizations for project: {project_id}")
        response = self.client.get(url, headers=headers)
        
        result = self._handle_response(response)
        authorizations = result.get("authorizations", [])
        logger.info(f"Found {len(authorizations)} authorizations")
        return {"authorizations": authorizations} 