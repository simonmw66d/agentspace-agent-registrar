import os
import urllib.parse
import httpx
import logging

from dotenv import load_dotenv

from as_agent_registry_service import get_access_token

load_dotenv()

logger = logging.getLogger(__name__)


def get_endpoint(location):
    if location == "global":
        return "discoveryengine.googleapis.com"
    else:
        if location[:2] in {"us", "eu"}:
            return f"{location}-discoveryengine.googleapis.com"
        
        raise ValueError(f"Invalid location: {location}")


def create_authorization(
    project_id: str, location: str, authorization_id: str, scopes: list[str]
):
    access_token = get_access_token()
    if not access_token:
        raise Exception("Failed to obtain access token for create_authorization.")

    url = f"https://{get_endpoint(location)}/v1alpha/projects/{project_id}/locations/{location}/authorizations?authorizationId={authorization_id}"
    query_string = urllib.parse.urlencode(
        {
            "client_id": os.getenv("OAUTH_CLIENT_ID"),
            "scope": " ".join(scopes),
            "include_granted_scopes": "true",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
        }
    )

    authorization_uri = f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    logger.debug(f"Authorization URI: {authorization_uri}")

    data = {
        "name": f"projects/{project_id}/locations/{location}/authorizations/{authorization_id}",
        "serverSideOauth2": {
            "clientId": os.getenv("OAUTH_CLIENT_ID"),
            "clientSecret": os.getenv("OAUTH_CLIENT_SECRET"),
            "authorizationUri": authorization_uri,
            "tokenUri": "https://oauth2.googleapis.com/token",
        },
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project_id,
    }
    response = httpx.post(url, json=data, headers=headers)
    response.raise_for_status()

    return response.json()


def delete_authorization(project_id: str, location: str, authorization_id: str):
    access_token = get_access_token()
    if not access_token:
        raise Exception("Failed to obtain access token for delete_authorization.")

    url = f"https://{get_endpoint(location)}/v1alpha/projects/{project_id}/locations/{location}/authorizations/{authorization_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project_id,
    }
    response = httpx.delete(url, headers=headers)
    response.raise_for_status()

    return response.json()


def list_authorizations(project_id: str, location: str):
    access_token = get_access_token()
    if not access_token:
        raise Exception("Failed to obtain access token for list_authorizations.")

    url = f"https://{get_endpoint(location)}/v1alpha/projects/{project_id}/locations/{location}/authorizations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project_id,
    }
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    print(list_authorizations("ai-ml-team-sandbox", "us"))