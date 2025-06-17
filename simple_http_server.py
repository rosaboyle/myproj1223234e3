#!/usr/bin/env python3
"""
Simple HTTP MCP Server using FastMCP

This provides a basic HTTP interface for the MCP calculator server.
"""

import logging
from mcp.server.fastmcp import FastMCP
import uvicorn
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP("simple-calculator")


@mcp.tool()
async def add_numbers(a: float, b: float) -> str:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of the two numbers
    """
    result = a + b
    return f"The sum of {a} and {b} is {result}"


@mcp.tool()
async def subtract_numbers(a: float, b: float) -> str:
    """Subtract two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The difference of the two numbers
    """
    result = a - b
    return f"The difference of {a} and {b} is {result}"


@mcp.tool()
async def multiply_numbers(a: float, b: float) -> str:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The product of the two numbers
    """
    result = a * b
    return f"The product of {a} and {b} is {result}"


@mcp.tool()
async def divide_numbers(a: float, b: float) -> str:
    """Divide two numbers.

    Args:
        a: First number (dividend)
        b: Second number (divisor)

    Returns:
        The quotient of the two numbers
    """
    if b == 0:
        return "Error: Cannot divide by zero"

    result = a / b
    return f"The quotient of {a} divided by {b} is {result}"


@mcp.tool()
async def get_info() -> str:
    """Get information about this MCP server.

    Returns:
        Information about the server and its capabilities
    """
    return """
    Simple Calculator MCP Server

    This server provides basic arithmetic operations:
    - Addition (add_numbers)
    - Subtraction (subtract_numbers)
    - Multiplication (multiply_numbers)
    - Division (divide_numbers)

    Transport: HTTP with FastMCP
    """


async def health_check(request):
    """Health check endpoint"""
    return JSONResponse(
        {
            "status": "healthy",
            "server": "simple-calculator-mcp",
            "tools": [
                "add_numbers",
                "subtract_numbers",
                "multiply_numbers",
                "divide_numbers",
                "get_info",
            ],
        }
    )


def create_app():
    """Create Starlette app with MCP integration"""
    # Create the FastMCP app
    fastmcp_app = mcp.create_app()

    # Create wrapper Starlette app for additional routes
    app = Starlette(
        routes=[
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

    # Mount the FastMCP app under /mcp
    app.mount("/mcp", fastmcp_app)

    return app


def main():
    """Run the HTTP server"""
    logger.info("Starting Simple Calculator MCP Server with HTTP transport...")

    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()
