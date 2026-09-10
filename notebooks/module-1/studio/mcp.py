"""09-mcp.ipynb — an agent whose tools come from a local MCP server.

The tools have to be fetched over stdio before the agent can be built, and that is
async. LangGraph accepts an async factory here: `langgraph.json` points at
`make_graph`, and the server awaits it at startup instead of at import time.
"""

import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER = Path(__file__).parent.parent / "resources" / "2.1_mcp_server.py"


async def make_graph(config=None):
    client = MultiServerMCPClient(
        {
            "local_server": {
                "transport": "stdio",
                # sys.executable, not "python" — this must be the venv interpreter
                "command": sys.executable,
                "args": [str(SERVER)],
            }
        }
    )

    tools = await client.get_tools()
    prompt = await client.get_prompt("local_server", "prompt")

    return create_agent(
        model="gpt-5-nano",
        tools=tools,
        system_prompt=prompt[0].content,
    )
