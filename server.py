# server.py
import os
from fastmcp import FastMCP

# --- Read n8n MCP config from environment ---
N8N_MCP_URL = os.environ["N8N_MCP_URL"]  # MCP Server Trigger Production URL
N8N_MCP_TOKEN = os.getenv("N8N_MCP_TOKEN")  # optional bearer token


# --- Build an MCPConfig-style proxy pointing at n8n ---
config = {
    "mcpServers": {
        # The name here (n8n) becomes the prefix if you ever proxy multiple servers.
        "n8n": {
            "url": N8N_MCP_URL,
            # This tells FastMCP to treat it as a Streamable HTTP MCP endpoint.
            "transport": "http",
        }
    }
}

# If we have a token, send it as Authorization: Bearer <token>
if N8N_MCP_TOKEN:
    config["mcpServers"]["n8n"]["headers"] = {
        "Authorization": f"Bearer {N8N_MCP_TOKEN}",
    }

# Create a proxy server that mirrors the remote n8n MCP server
# This will forward tools, resources, prompts, etc.
proxy = FastMCP.as_proxy(config, name="n8n-proxy")


if __name__ == "__main__":
    # Railway gives us PORT; default to 8000 locally
    port = int(os.environ.get("PORT", "8000"))

    # Expose the proxy over HTTP (Streamable HTTP transport)
    # The MCP endpoint will be: http(s)://<railway-domain>/mcp
    proxy.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        path="/mcp",
    )

