#!/usr/bin/env python3
"""
Simple MCP Server Template with Streamable HTTP Transport

This is a basic Model Context Protocol (MCP) server template that demonstrates:
- Simple tool implementation using FastMCP
- Basic server setup
- STDIO transport (can be modified for HTTP)

The server provides a simple calculator tool as an example.
"""

import logging
from mcp.server.fastmcp import FastMCP

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
async def calculate_power(base: float, exponent: float) -> str:
    """Calculate base raised to the power of exponent.

    Args:
        base: Base number
        exponent: Exponent

    Returns:
        The result of base^exponent
    """
    result = base ** exponent
    return f"{base} raised to the power of {exponent} is {result}"


@mcp.tool()
async def get_info() -> str:
    """Get information about this MCP server.

    Returns:
        Information about the server and its capabilities
    """
    return """
    This is a simple MCP calculator server that provides basic arithmetic operations:
    - Addition
    - Subtraction
    - Multiplication
    - Division
    - Power/Exponentiation

    The server uses the Model Context Protocol with FastMCP.
    """


def main():
    """Main function to run the MCP server."""
    logger.info("Starting Simple Calculator MCP Server...")

    # Run the server with STDIO transport
    # For HTTP transport, use the http_server.py implementation instead
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
