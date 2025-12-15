## MCP Weather Agent

Small MCP-compatible weather toolkit that wraps National Weather Service alerts and forecasts as tools, plus example clients for SSE and chat-driven usage.

### Suggested repository name
- `mcp-weather-agent`

### Features
- MCP server exposing `get_alerts` and `get_forecast` against NWS.
- SSE client demo that lists tools and invokes `get_alerts`.
- Chat client using `mcp-use` + `ChatGroq` with built-in memory.
- Minimal entry stub in `main.py`.

### Structure
- `mcpserver/server.py` — FastMCP server (default SSE on port 8000).
- `mcpserver/client-sse.py` — Example SSE client.
- `graphqlserver/graphql_example.py` — GraphQL MCP server (Rick and Morty).
- `graphqlserver/client.py` — Chat client for the GraphQL server (`graphql.json`).
- `server/client.py` — Chat client configured via `server/weather.json`.
- `server/weather.py` — Alternate FastMCP server example.
- `main.py` — Simple script stub.

### Requirements
- Python 3.11+
- `uv` (recommended) or `pip`
- `GROQ_API_KEY` for the chat client

### Setup
Using uv:
```bash
uv sync
```

Using pip:
```bash
python -m venv .venv
source .venv/bin/activate
uv pip compile uv.lock > requirements.txt  # optional helper
pip install -r requirements.txt
```

### Run the MCP weather server (SSE)
```bash
uv run mcpserver/server.py
```
Defaults: host `0.0.0.0`, port `8000`, SSE transport.

### Inspect with MCP Inspector
```bash
uv run mcp dev server/weather.py
```
Opens MCP Inspector and proxy for the `server/weather.py` MCP server (stdio transport).

### Try the SSE client
```bash
uv run mcpserver/client-sse.py
```
Assumes the server is running on `http://localhost:8000/sse`.

### Chat with the MCP tools (Groq + memory)
```bash
export GROQ_API_KEY=your_key
uv run server/client.py
```
- Uses `server/weather.json` for MCP client configuration.
- Commands: `clear` wipes conversation history; `exit`/`quit` stops.

### Using GraphQL APIs

You can create MCP tools that interact with any open-source GraphQL API! See `mcpserver/graphql_example.py` for an example using the [Rick and Morty GraphQL API](https://rickandmortyapi.com/graphql).

**Run the GraphQL example server:**
```bash
uv run graphqlserver/graphql_example.py
```
Runs on port 8001 with a single tool for querying Rick and Morty characters.

**Available tools:**
- `get_character(character_id)` - Get character details by ID

**Chat client for the GraphQL server:**
```bash
export GROQ_API_KEY=your_key
uv run graphqlserver/client.py
```
Uses `graphqlserver/graphql.json` to start the MCP server and chat with the `get_character` tool.

**To create your own GraphQL tools:**
1. Use the `make_graphql_request()` helper function from `graphql_example.py`
2. Write your GraphQL query as a string
3. Create an `@mcp.tool()` decorated function
4. Call `make_graphql_request()` with your API endpoint, query, and variables

### Notes
- NWS requires a user agent; the server sets `weather-app/1.0`.
- Forecasts return the next five periods for brevity.
- GraphQL tools use `httpx` for HTTP requests (already included in dependencies).
