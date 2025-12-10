## MCP Weather Agent

A small MCP-compatible weather toolkit that exposes National Weather Service alerts and forecasts as tools, plus example clients for SSE and chat-driven usage.

### Suggested repository name
- `mcp-weather-agent`

### What’s here
- `mcpserver/server.py`: FastMCP server exposing `get_alerts` and `get_forecast` via NWS.
- `mcpserver/client-sse.py`: Example SSE client that lists tools and calls `get_alerts`.
- `server/client.py`: Chat client using `mcp-use` + `ChatGroq` with built-in conversation memory.
- `main.py`: Simple entry script stub.

### Prerequisites
- Python 3.11+
- `uv` (recommended) or `pip`
- A `GROQ_API_KEY` in your environment for the chat client

### Setup
Using uv:
```bash
uv sync
```

Using pip:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or `uv pip compile uv.lock > requirements.txt` first
```

### Run the MCP weather server (SSE)
```bash
uv run mcpserver/server.py
```
Defaults: host `0.0.0.0`, port `8000`, SSE transport.

### Try the SSE client example
```bash
uv run mcpserver/client-sse.py
```
Assumes the server is already running on `http://localhost:8000/sse`.

### Chat with the MCP tools (Groq + memory)
```bash
export GROQ_API_KEY=your_key
uv run server/client.py
```
- Uses `server/weather.json` for MCP client configuration.
- Supports `clear` to wipe conversation history and `exit`/`quit` to stop.

### Notes
- NWS requires a user agent; this is set in the server code (`weather-app/1.0`).
- Forecasts return the next five periods for brevity.
