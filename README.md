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