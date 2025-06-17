#!/usr/bin/env python3
"""
MCP Streamable HTTP Server Template
Simple calculator server using proper MCP StreamableHTTPSessionManager
"""

import contextlib
import logging
from collections.abc import AsyncIterator

import click
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--port", default=8002, help="Port to listen on for HTTP")
@click.option(
    "--log-level",
    default="INFO",
    help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
@click.option(
    "--json-response",
    is_flag=True,
    default=False,
    help="Enable JSON responses instead of SSE streams",
)
def main(
    port: int,
    log_level: str,
    json_response: bool,
) -> int:
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create MCP server
    app = Server("simple-calculator-mcp")

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.Content]:
        """Handle tool calls for calculator operations"""
        try:
            if name == "add_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                result = a + b
                return [
                    types.TextContent(
                        type="text", text=f"The sum of {a} and {b} is {result}"
                    )
                ]

            elif name == "subtract_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                result = a - b
                return [
                    types.TextContent(
                        type="text", text=f"The difference of {a} and {b} is {result}"
                    )
                ]

            elif name == "multiply_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                result = a * b
                return [
                    types.TextContent(
                        type="text", text=f"The product of {a} and {b} is {result}"
                    )
                ]

            elif name == "divide_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 1)
                if b == 0:
                    return [
                        types.TextContent(
                            type="text", text="Error: Cannot divide by zero"
                        )
                    ]
                result = a / b
                return [
                    types.TextContent(
                        type="text",
                        text=f"The quotient of {a} divided by {b} is {result}",
                    )
                ]

            elif name == "power":
                base = arguments.get("base", 0)
                exponent = arguments.get("exponent", 1)
                result = base**exponent
                return [
                    types.TextContent(
                        type="text",
                        text=f"{base} raised to the power of {exponent} is {result}",
                    )
                ]

            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available calculator tools"""
        return [
            types.Tool(
                name="add_numbers",
                description="Add two numbers together",
                inputSchema={
                    "type": "object",
                    "required": ["a", "b"],
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"},
                    },
                },
            ),
            types.Tool(
                name="subtract_numbers",
                description="Subtract second number from first",
                inputSchema={
                    "type": "object",
                    "required": ["a", "b"],
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"},
                    },
                },
            ),
            types.Tool(
                name="multiply_numbers",
                description="Multiply two numbers",
                inputSchema={
                    "type": "object",
                    "required": ["a", "b"],
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"},
                    },
                },
            ),
            types.Tool(
                name="divide_numbers",
                description="Divide first number by second",
                inputSchema={
                    "type": "object",
                    "required": ["a", "b"],
                    "properties": {
                        "a": {"type": "number", "description": "Dividend"},
                        "b": {"type": "number", "description": "Divisor"},
                    },
                },
            ),
            types.Tool(
                name="power",
                description="Raise base to exponent power",
                inputSchema={
                    "type": "object",
                    "required": ["base", "exponent"],
                    "properties": {
                        "base": {"type": "number", "description": "Base number"},
                        "exponent": {"type": "number", "description": "Exponent"},
                    },
                },
            ),
        ]

    # Create the session manager (stateless mode)
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,  # No event store = stateless
        json_response=json_response,
        stateless=True,
    )

    # ASGI handler for streamable HTTP connections
    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(starlette_app: Starlette) -> AsyncIterator[None]:
        """Context manager for session manager lifecycle"""
        async with session_manager.run():
            logger.info(
                "🚀 Simple Calculator MCP Server with Streamable HTTP transport started!"
            )
            logger.info(f"📍 Server running on http://127.0.0.1:{port}")
            logger.info(f"🔗 MCP endpoint: http://127.0.0.1:{port}/mcp")
            try:
                yield
            finally:
                logger.info("Application shutting down...")

    # Create Starlette ASGI application
    starlette_app = Starlette(
        debug=True,
        routes=[
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )

    # Run with uvicorn
    import uvicorn

    uvicorn.run(starlette_app, host="127.0.0.1", port=port)

    return 0


if __name__ == "__main__":
    main()
