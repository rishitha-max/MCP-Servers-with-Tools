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

### Notes
- NWS requires a user agent; the server sets `weather-app/1.0`.
- Forecasts return the next five periods for brevity.
