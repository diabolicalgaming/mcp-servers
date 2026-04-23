#1. Import FastMPC
from mcp.server.fastmcp import FastMCP

# 2. Initialize MCP Server
mcp = FastMCP(name="server-name")

# 3. TOOLS - finctions that do things
# Add your tool definitions here using the @mcp.tool decorator. Functions that perform actions/operations are marked with @mcp.tool()

# 4. RESOURCES - data endpoints
'''
    @mcp.resource() is for data that already exists — think of it like a REST GET endpoint. 
    It's meant for reading relatively stable, pre-existing data. Good examples: reading a config file, 
    returning cached state, exposing a database record by ID.

    The key distinction: resources are expected to be cheap, idempotent reads. 
    Tools are for operations that do meaningful work.
'''
# Add your resource definitions here using the @mcp.resource decorator. Functions that return data/information are marked with @mcp.resource()

# 5. PROMPTS - AI assistance templates
# Add your prompt definitions here using the @mcp.prompt decorator. Use @mcp.prompt() when you want to export prompt templates for clients to use with their own LLM. For example if I am using Kiro, then this Kiro is the client in this case.

#6. Run the server
def main():

    # Stateful server (maintains session state)
    mcp = FastMCP("StatefulServer")

    # Stateless server (no session persistence)
    mcp = FastMCP("StatelessServer", stateless_http=True)

    # Run server with stdio transport
    mcp.run(transport="stdio")

    # Run server with streamable-http transport
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
