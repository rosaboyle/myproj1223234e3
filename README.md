# Python MCP Server Template with Streamable HTTP Transport

This template provides multiple implementations of a simple calculator MCP (Model Context Protocol) server using different approaches for HTTP transport.

## Server Implementations

### 1. STDIO Server (`main.py`) - Working
Simple MCP server using STDIO transport (CLI-based).
```bash
python main.py
```

### 2. Manual HTTP Server (`http_server.py`) - Working  
Custom HTTP server with manual JSON-RPC handling.
- Port: 8001
- Endpoint: `http://localhost:8001/mcp`
- Health Check: `http://localhost:8001/health`

```bash
python http_server.py
```

### 3. Streamable HTTP Server (`streamable_server.py`) - Working
Proper MCP streamable HTTP server using `StreamableHTTPSessionManager` (stateless).
- Port: 8002  
- Endpoint: `http://localhost:8002/mcp`
- Features: Stateless, efficient streaming

```bash
python streamable_server.py
# or with options:
python streamable_server.py --port 8002 --log-level INFO
```

### 4. Stateful Streamable Server (`stateful_server.py`) - Available
Stateful MCP server with event store for resumability.
- Port: 8003
- Endpoint: `http://localhost:8003/mcp` 
- Features: Event store, resumability, progress notifications

```bash
python stateful_server.py
# or with options:
python stateful_server.py --port 8003 --json-response
```

## Setup

1. Create Virtual Environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

## Available Tools

All server implementations provide the same calculator tools:

- add_numbers - Add two numbers together
- subtract_numbers - Subtract second number from first  
- multiply_numbers - Multiply two numbers
- divide_numbers - Divide first number by second
- power - Raise base to exponent power
- slow_calculation - (Stateful server only) Demonstrates streaming with progress

## Testing

### HTTP Client
A simple HTTP client is provided to test the servers:

```bash
cd ../mcp-http-client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python client.py
```

The client automatically detects which server is running (ports 8001-8003) and tests all functionality.

### Manual Testing with cURL

Initialize:
```bash
curl -X POST http://localhost:8002/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}'
```

List Tools:
```bash
curl -X POST http://localhost:8002/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}'
```

Call Tool:
```bash
curl -X POST http://localhost:8002/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "add_numbers", "arguments": {"a": 5, "b": 3}}}'
```

## Architecture

### Recommended Approach: Streamable HTTP
The streamable_server.py is the recommended implementation as it:
- Uses the official StreamableHTTPSessionManager
- Follows MCP best practices
- Supports proper streaming
- Is stateless and efficient
- Handles all MCP protocol details automatically

### Manual HTTP (Legacy)
The http_server.py shows manual JSON-RPC handling for educational purposes but is not recommended for production.

### Stateful Version
The stateful_server.py demonstrates advanced features:
- Event store for resumability
- Progress notifications during tool execution
- Stream persistence and replay capabilities

## Claude Desktop Integration

Add to your Claude Desktop config (claude_desktop_config.json):

```json
{
  "mcpServers": {
    "simple-calculator": {
      "command": "python",
      "args": ["/path/to/python-streamable-http/main.py"],
      "env": {}
    }
  }
}
```

For HTTP transport, use appropriate endpoints in your MCP client configuration.

## File Structure

```
python-streamable-http/
├── main.py                 # STDIO server (FastMCP)
├── http_server.py          # Manual HTTP server  
├── streamable_server.py    # Streamable HTTP server (recommended)
├── stateful_server.py      # Stateful server with event store
├── event_store.py          # Event store implementation
├── simple_http_server.py   # Legacy FastMCP HTTP attempt
├── test_mcp.py            # STDIO test script
├── requirements.txt        # Dependencies
├── pyproject.toml         # Project metadata
└── README.md              # This file

mcp-http-client/
├── client.py              # HTTP client for testing
├── requirements.txt       # Client dependencies  
└── README.md              # Client documentation
```

## Next Steps

1. For Learning: Start with streamable_server.py to understand proper MCP implementation
2. For Production: Use streamable_server.py for stateless applications or stateful_server.py for resumable operations
3. For Integration: Adapt the tool implementations for your specific use case
4. For Advanced Features: Extend with resources, prompts, or custom streaming logic

## Performance Notes

- Streamable HTTP: Best performance, handles concurrent requests efficiently
- Manual HTTP: Educational only, not optimized for production
- STDIO: Perfect for CLI usage and Claude Desktop integration
- Stateful: Adds overhead for persistence but enables resumability
