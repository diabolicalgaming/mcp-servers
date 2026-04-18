from mcp.client.session import ClientSession
import asyncio

async def client():
    client = ClientSession("http://localhost:8080/mcp")

    async with client:
        # List what's available
        tools = await client.list_tools()

        # Use tools
        flights = await client.call_tool("search_flights", {
            "origin": "SFO",
            "destination": "JFK"
        })

        # Read resources
        status = await client.read_resource("flight://status/UA123")

        # Get prompts
        advice = await client.get_prompt("find_flight", {
            "details": "SFO to JFK"
        })
    
asyncio.run(client())