#!/usr/bin/env python3
"""
Test script for the MCP server
"""

import asyncio
import json


async def test_mcp_server():
    """Test the MCP server functionality"""

    # Test 1: Initialize
    print("=== Testing MCP Server ===")
    print("1. Testing initialization...")

    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }

    # Test initialization
    print(f"Request: {json.dumps(init_request, indent=2)}")

    # Test 2: List tools
    print("\n2. Testing list tools...")

    list_tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

    print(f"Request: {json.dumps(list_tools_request, indent=2)}")

    # Test 3: Call a tool
    print("\n3. Testing tool call...")

    tool_call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "add_numbers", "arguments": {"a": 5, "b": 3}},
    }

    print(f"Request: {json.dumps(tool_call_request, indent=2)}")

    print("\n=== Manual Testing Instructions ===")
    print("To test the MCP server manually, run:")
    print("source .venv/bin/activate")
    print("python main.py")
    print()
    print("Then in another terminal, send these JSON-RPC requests:")
    print("1. Initialize:")
    print(json.dumps(init_request))
    print()
    print("2. List tools:")
    print(json.dumps(list_tools_request))
    print()
    print("3. Call add_numbers:")
    print(json.dumps(tool_call_request))


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
