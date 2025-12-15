"""
Example MCP server with GraphQL API integration.

This demonstrates how to create MCP tools that interact with GraphQL APIs.
Uses the Rick and Morty GraphQL API: https://rickandmortyapi.com/graphql

You can adapt this pattern for any open-source GraphQL API.
"""

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(
    name="rick-morty-graphql",
    host="0.0.0.0",
    port=8001,  # Different port from weather server
)

# Rick and Morty GraphQL API endpoint (public, no auth required)
RICK_MORTY_GRAPHQL_URL = "https://rickandmortyapi.com/graphql"


async def make_graphql_request(
    url: str,
    query: str,
    variables: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any] | None:
    """
    Make a GraphQL request to any GraphQL API endpoint.
    
    Args:
        url: GraphQL API endpoint URL
        query: GraphQL query string
        variables: Optional variables for the query
        headers: Optional headers (for auth, etc.)
    """
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    default_headers = {"Content-Type": "application/json"}
    if headers:
        default_headers.update(headers)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                json=payload,
                headers=default_headers,
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            
            # Check for GraphQL errors
            if "errors" in result:
                error_messages = [err.get("message", "Unknown error") for err in result["errors"]]
                raise Exception(f"GraphQL errors: {', '.join(error_messages)}")
            
            return result.get("data")
        except httpx.HTTPStatusError as e:
            return None
        except Exception as e:
            return None


@mcp.tool()
async def get_character(character_id: int) -> str:
    """Get information about a Rick and Morty character by ID.
    
    Args:
        character_id: Character ID (1-826)
    """
    query = """
    query GetCharacter($id: ID!) {
        character(id: $id) {
            name
            status
            species
            type
            gender
            origin {
                name
            }
            location {
                name
            }
            image
        }
    }
    """
    
    variables = {"id": str(character_id)}
    data = await make_graphql_request(RICK_MORTY_GRAPHQL_URL, query, variables)
    
    if not data or "character" not in data:
        return "Unable to fetch character information."
    
    char = data["character"]
    if not char:
        return f"Character with ID {character_id} not found."
    
    return f"""
    Name: {char.get('name', 'Unknown')}
    Status: {char.get('status', 'Unknown')}
    Species: {char.get('species', 'Unknown')}
    Type: {char.get('type', 'N/A')}
    Gender: {char.get('gender', 'Unknown')}
    Origin: {char.get('origin', {}).get('name', 'Unknown')}
    Location: {char.get('location', {}).get('name', 'Unknown')}
    Image: {char.get('image', 'N/A')}
    """


@mcp.tool()
async def get_episode(episode_id: int) -> str:
    """Get information about a Rick and Morty episode by ID.

    Args:
        episode_id: Episode ID (1-51)
    """
    query = """
    query GetEpisode($id: ID!) {
        episode(id: $id) {
            name
            air_date
            episode
            characters {
                name
            }
        }
    }
    """

    variables = {"id": str(episode_id)}
    data = await make_graphql_request(RICK_MORTY_GRAPHQL_URL, query, variables)

    if not data or "episode" not in data:
        return "Unable to fetch episode information."

    episode = data["episode"]
    if not episode:
        return f"Episode with ID {episode_id} not found."

    characters = ", ".join([char["name"] for char in episode.get("characters", [])[:10]])

    return f"""
    Episode: {episode.get('name', 'Unknown')}
    Air Date: {episode.get('air_date', 'Unknown')}
    Episode Code: {episode.get('episode', 'Unknown')}
    Characters: {characters or 'N/A'}
    """


# Run the server
if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running Rick and Morty GraphQL server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running Rick and Morty GraphQL server with SSE transport on port 8001")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")
