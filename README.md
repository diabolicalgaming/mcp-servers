# MCP Servers

## Model Context Protocol (MCP):

**Model Context Protocol (MCP)** extends Kiro's capabilities by connecting to specialized servers that provide additional tools and context.

## What is MCP?

* **Model Context Protocol (MCP)** - is a protocol that allows Kiro to communicate with external servers to access specialized tools, prompts, and resources.

For example, the AWS documentation MCP server provides tools to search, read, and get recommendations from AWS documentation directly within Kiro.

With MCP, you can:

* Access specialized knowledge bases and documentation.
* Integrate with external services and APIs.
* Extend Kiro's capabilities with domain-specific tools.
* Use server-provided prompt templates and resources via the # mention system in chat.
* Respond to server elicitation requests when tools need additional input during execution.
* Create custom tools for your specific workflows.

### Context7

* **Context7** - is an open-source MCP server designed to eliminate AI hallucinations by providing up-to-date, version-specific documentation to LLMs and AI code editors like Cursor, Windsurf, and VS Code.

Context7 acts as a bridge that fetches the latest API documentation, reducing reliance on outdated training data.

In the steering file, make sure to set a rule for Context7 whenever we are using **Agent Hooks** or **Specs**.

#### Usage Examples:

* **Prompting with ```use context7```** - within an AI agent (like Cursor), you can type ```use context7 [library name][task]``` to get accurate code examples.
* **Integrating with MCP** - set up Context7 as an MCP server to automatically allow AI assistants to fetch documentation, such as asking to ***show the Supabase auth API for email/password sign-up***.
* **Targeting specific frameworks** - it is commonly used to ensure correct syntax for rapidly evolving libraries, such as Next.js, Cloudflare Workers, or Supabase.

## Why MCP Servers

Essentially Agent Agent use MCP servers to connect to existing API documentation of existing tools to be able to make decisions.

## MCP Breakdown

* **Model** - refers to the AI/LLM's.
* **Context** - giving AI context of a third-party.
* **Protocol** - a set of standards.

So, MCP itself are just a set of standards that define how AI applications can work with each other.

## MCP Architechture

### Primitives

**MCP Primitives** are the most important concept within MCP. They define what clients and servers can offer each other. These primitives specify the types of contextual information that can be shared with AI applications and the range of actions that can be performed.

* **Tools** - executable functions that AI applications can invoke to perform actions (e.g., file operations, API calls, database queries).
* **Resources** - data sources that provide contextual information to AI applications (e.g. file contents, database records, API response).
* **Prompts** - reusable templates that help structure interactions with language models (e.g., system prompts, few-shot examples).

### JSON-RCP 2.0

* **JSON Remote Procedure Call (JSON-RCP)** - is a lightweight, statelss remote procedure call (RPC) that uses JSON for encoding messages.

JSON-RPC allows a client to invoke methods on a server remotely, passing parameters and receiving results via a simple text-based format. It is transport-agnostic, supporting HTTP, WebSockets, and more.

Example Python Code:
```python
def add(a: float, b: float):
    return Success(a+b)

rpc_request = request("add", {3,2})
```

Example JSON-RPC (2.0) request:
```json
{
    "jsonrpc": "2.0",
    "method": "add",
    "params": {
        "a": 10,
        "b": 5
    },
    "id": 42
}
```

Example JSON-RPC (2.0) response:
```json
{
    "jsonrpc" : "2.0",
    "result": 15,
    "error": {} // if error
    "id": 42
}
```

Note that JSON-RPC is a simple protocol as such it is stateless and does not define how data is transmitted between client and server. That's up for us to decide. It could be ***HTTP*** or ***STDIO*** which MCP supports as the transport mechanism for client to server communication.

## Use Existing MCP Server

MCP servers can be locally or remotely hosted by the vendor themselves.

MCP Server Example:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": [
        "-y", "@upstash/context7-mcp"
      ],
      "env": {},
      "disabled": false,
      "autoApprove": [
        "resolve-library-id",
	      "get-library-docs"
      ]
    }
  }
}
```

## MCP Inspector

* **MCP Inspector** - is an interactive developer tool for testing and debugging MCP servers.

To use the MCP Inspector run the following command:

```shell
npx @modelcontextprotocol/inspector
```

The MCP Inspector runs on http://localhost:6274/


### Creating flight-booking-server MCP

```
uv init flight-booking-server
cd flight-booking-server
uv add "mcp[cli]"
```

Here is the code for ***server.py***:

```python
import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Flight Booking Server")

@mcp.resource("file://airports")  # type: ignore[misc]
def get_airports() -> str:
    return json.dumps({
        "LAX": {"name": "Los Angeles International", "city": "Los Angeles"},
        "JFK": {"name": "John F. Kennedy International", "city": "Washington"},
        "LHR": {"name": "London Heathrow", "city": "London"}
    })

@mcp.tool()  # type: ignore[misc]
def create_booking(flight_id: str, passenger_name: str) -> dict[str, str]:
    return {
        "booking_id": f"BK{flight_id}[-3]",
        "flight_id": flight_id,
        "passenger": passenger_name,
        "status": "confirmed"
    }

@mcp.prompt()
def find_best_flight(budget: float, preferences: str = "economy") -> str:
    return f"Generate a prompt for finding the best flight within budget {budget}. My seeting preference is {preferences}"



def main() -> None:
    pass


if __name__ == "__main__":
    pass
```

Here is the ***mcp.json** file:
```json
{
    "mcpServers" : {
        "flight-booking": {
            "command": "uv",
            "args": ["run", "python", "server.py"],
            "cwd": "/Users/taaibor1/repos/mine/mcp-servers/flight-booking-server"
        }
    }
}
```

## MCP Client

* **MCP Client** - is an application, typically an **AI agent**, **chat interface**, or **IDE** that acts as the intiator in the MCP ecosystem, allowing LLMs to securely connect with external data sources and tools, such as databases, APIs, or local files.

A lot of agents support MCP clients automatically, e.g. Cursor or Claude Code have an ***mcp.json** configuration file that simply needs to be configured to point to the MCP servers.

However, if you would like to build your own AI agent, you might want to build the client from scratch.

The important features in an MCP Client are:

* **Roots** - allow clients to specify which directories servers should focus on, communicating intended scope through a coordination mechanism.
* **Sampling** - allows servers to request LLM completions through the client, enabling an agentic workflow. This approach puts the client in complete control of user permissions and security measures.
* **Elicitation** - enables servers to request specific information from users during interactions, providing a structured way for servers to gather information on demand.

### Sample MCP Server to Client code

Here is example code for a MCP server
```
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
```

Here is a sample code for its MCP client
```
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
```

### Contexts 

Contexts allow the server to talk back to the client, i.e. to give updates or sharing progress etc.

Here is example code using Context:
```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP(name="Progress Example")

@mcp.tool()
async def long_running_task(task_name: str, ctx: Context, steps: int = 5) -> str:
    await ctx.info(f"Starting: {task_name}")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Step {i + 1}/{steps}"
        )
        await ctx.debug(f"Completed step {i + 1}")
    
    return f"Task '{task_name}' completed"
```