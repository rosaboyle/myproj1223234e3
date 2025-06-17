#!/usr/bin/env python3
"""
MCP Server with Streamable HTTP Transport

This implementation provides a proper HTTP transport for MCP servers
following the MCP specification for streamable HTTP.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route
import uvicorn

from mcp.server import Server
from mcp.types import Tool, TextContent


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleCalculatorServer:
    """Simple Calculator MCP Server with HTTP Transport"""

    def __init__(self):
        self.server = Server("simple-calculator")
        self.setup_handlers()

    def setup_handlers(self):
        """Set up MCP message handlers"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="add_numbers",
                    description="Add two numbers together",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "number",
                                "description": "First number"
                            },
                            "b": {
                                "type": "number",
                                "description": "Second number"
                            }
                        },
                        "required": ["a", "b"]
                    }
                ),
                Tool(
                    name="subtract_numbers",
                    description="Subtract two numbers",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "number",
                                "description": "First number"
                            },
                            "b": {
                                "type": "number",
                                "description": "Second number"
                            }
                        },
                        "required": ["a", "b"]
                    }
                ),
                Tool(
                    name="multiply_numbers",
                    description="Multiply two numbers",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "number",
                                "description": "First number"
                            },
                            "b": {
                                "type": "number",
                                "description": "Second number"
                            }
                        },
                        "required": ["a", "b"]
                    }
                ),
                Tool(
                    name="divide_numbers",
                    description="Divide two numbers",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "a": {
                                "type": "number",
                                "description": "Dividend"
                            },
                            "b": {
                                "type": "number",
                                "description": "Divisor"
                            }
                        },
                        "required": ["a", "b"]
                    }
                ),
                Tool(
                    name="get_server_info",
                    description="Get information about this MCP server",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""

            if name == "add_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                result = a + b
                text = f"The sum of {a} and {b} is {result}"
                return [TextContent(type="text", text=text)]

            elif name == "subtract_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                result = a - b
                text = f"The difference of {a} and {b} is {result}"
                return [TextContent(type="text", text=text)]

            elif name == "multiply_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 0)
                result = a * b
                text = f"The product of {a} and {b} is {result}"
                return [TextContent(type="text", text=text)]

            elif name == "divide_numbers":
                a = arguments.get("a", 0)
                b = arguments.get("b", 1)
                if b == 0:
                    return [TextContent(
                        type="text",
                        text="Error: Cannot divide by zero"
                    )]
                result = a / b
                text = f"The quotient of {a} divided by {b} is {result}"
                return [TextContent(type="text", text=text)]

            elif name == "get_server_info":
                info = """
                Simple Calculator MCP Server

                This server provides basic arithmetic operations:
                - Addition (add_numbers)
                - Subtraction (subtract_numbers)
                - Multiplication (multiply_numbers)
                - Division (divide_numbers)

                Transport: Streamable HTTP
                Protocol Version: MCP 2024-11-05
                """
                return [TextContent(type="text", text=info.strip())]

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]


    async def add_numbers(self, a, b):
        result = a + b
        return f"The sum of {a} and {b} is {result}"

    async def subtract_numbers(self, a, b):
        result = a - b
        return f"The difference of {a} and {b} is {result}"

    async def multiply_numbers(self, a, b):
        result = a * b
        return f"The product of {a} and {b} is {result}"

    async def divide_numbers(self, a, b):
        if b == 0:
            return "Error: Cannot divide by zero"
        result = a / b
        return f"The quotient of {a} divided by {b} is {result}"

    async def power(self, base, exponent):
        result = base ** exponent
        return f"{base} raised to the power of {exponent} is {result}"


# Global server instance
calculator_server = SimpleCalculatorServer()


async def handle_mcp_request(request: Request) -> JSONResponse:
    """Handle MCP JSON-RPC requests via HTTP POST"""
    try:
        # Parse JSON-RPC request
        body = await request.body()
        json_rpc_request = json.loads(body)

        logger.info(f"Received MCP request: {json_rpc_request}")

        # Extract request details
        method = json_rpc_request.get("method")
        params = json_rpc_request.get("params", {})
        request_id = json_rpc_request.get("id")

        # Handle different MCP methods manually
        if method == "initialize":
            # Handle initialization
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "simple-calculator",
                    "version": "1.0.0"
                }
            }
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        elif method == "tools/list":
            # Handle tools list
            tools = [
                {
                    "name": "add_numbers",
                    "description": "Add two numbers together",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "subtract_numbers", 
                    "description": "Subtract second number from first",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "multiply_numbers",
                    "description": "Multiply two numbers",
                    "inputSchema": {
                        "type": "object", 
                        "properties": {
                            "a": {"type": "number", "description": "First number"},
                            "b": {"type": "number", "description": "Second number"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "divide_numbers",
                    "description": "Divide first number by second",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "Dividend"},
                            "b": {"type": "number", "description": "Divisor"}
                        },
                        "required": ["a", "b"]
                    }
                },
                {
                    "name": "power",
                    "description": "Raise base to exponent power",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "base": {"type": "number", "description": "Base number"},
                            "exponent": {"type": "number", "description": "Exponent"}
                        },
                        "required": ["base", "exponent"]
                    }
                }
            ]
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": tools}
            }

        elif method == "tools/call":
            # Handle tool calls
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            try:
                if tool_name == "add_numbers":
                    result_text = await calculator_server.add_numbers(arguments["a"], arguments["b"])
                elif tool_name == "subtract_numbers":
                    result_text = await calculator_server.subtract_numbers(arguments["a"], arguments["b"])
                elif tool_name == "multiply_numbers":
                    result_text = await calculator_server.multiply_numbers(arguments["a"], arguments["b"])
                elif tool_name == "divide_numbers":
                    result_text = await calculator_server.divide_numbers(arguments["a"], arguments["b"])
                elif tool_name == "power":
                    result_text = await calculator_server.power(arguments["base"], arguments["exponent"])
                else:
                    raise ValueError(f"Unknown tool: {tool_name}")
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result_text
                            }
                        ]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error: {str(e)}"
                            }
                        ],
                        "isError": True
                    }
                }

        else:
            # Unknown method
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

        logger.info(f"Sending MCP response: {response}")
        return JSONResponse(content=response)

    except json.JSONDecodeError:
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            },
            status_code=400
        )
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": json_rpc_request.get("id") if 'json_rpc_request' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            },
            status_code=500
        )


async def handle_mcp_sse(request: Request) -> StreamingResponse:
    """Handle Server-Sent Events for MCP (optional)"""
    async def generate():
        yield "data: {\"type\": \"connection_established\"}\n\n"
        # Keep connection alive
        await asyncio.sleep(1)
        yield "data: {\"type\": \"ping\"}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "server": "simple-calculator-mcp"
    })


# Create Starlette application
app = Starlette(
    routes=[
        Route("/mcp", handle_mcp_request, methods=["POST"]),
        Route("/mcp", handle_mcp_sse, methods=["GET"]),
        Route("/health", health_check, methods=["GET"]),
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    """Run the HTTP server"""
    logger.info("Starting Simple Calculator MCP Server with HTTP transport...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )


if __name__ == "__main__":
    main()
