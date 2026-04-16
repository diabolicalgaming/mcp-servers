from mcp.server.fastmcp import FastMCP

mcp = FastMCP("flight-server")

@mcp.tool()
async def search_flights(origin: str, destination: str)
    return {"flights": ["flights1", "flights2"]}

@mcp.resource("flight://status/{id}")
async def get_status(id: str):
    return {"status": "on_time"}

@mcp.prompt()
async def find_flight(details: str):
    return f"Suggestions for {details}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8080)