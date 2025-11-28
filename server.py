# server.py
import asyncio
import os

from fastmcp import FastMCP, Client  # uses the FastMCP library in the repo

N8N_MCP_URL = os.environ["N8N_MCP_URL"]  # set this in Railway (you already did)
N8N_MCP_TOKEN = os.environ.get("N8N_MCP_TOKEN")  # optional auth token for n8n


async def build_proxy() -> FastMCP:
    """
    Build a FastMCP proxy that forwards everything to your n8n MCP server.
    This makes your Railway service look like a 'proper' MCP server
    to ChatGPT / connectors.
    """
    # FastMCP Client auto-detects HTTP/SSE transport from the URL
    client = Client(
        N8N_MCP_URL,
        auth=N8N_MCP_TOKEN,  # if set, will be sent as Authorization: Bearer <token> 
    )

    proxy = await FastMCP.as_proxy(
        client,
        name="n8n-proxy",
    )
    return proxy


if __name__ == "__main__":
    proxy = asyncio.run(build_proxy())

    # Railway injects PORT; default to 8000 locally
    port = int(os.environ.get("PORT", "8000"))

    # Expose as Streamable HTTP MCP server at /mcp
    proxy.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )
