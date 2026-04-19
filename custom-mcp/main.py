# Tutorial: https://github.com/modelcontextprotocol/python-sdk

import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AI Sticky Notes")
NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

def ensure_file() -> None:
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")


"""
    It's important to specify types so that the AI agent knows how to pass them.
    The message parameter is passed by the AI agent when it calls this tool. 
    The return type is what the AI agent will receive as a response after calling this tool.
    
    Make sure to add the docstring to explain what the tool does, and what the parameters are for. 
    This will help the AI agent understand how to use it.
"""
@mcp.tool()
def add_note(message: str) -> str:
    # Below is a docstring
    """
    Append a new note to the sticky note file.

    :param: message (str): the note content to be added.
    :return: str: Confirmation message indicating the note was saved.
    """
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note saved!"

@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the sticky note file.

    :return: str: All notes as a single string separated by line breaks. If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    return content or "No notes found."

# You use mcp.resource() to read information
@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the most recently added note from the sticky note file.

    :return: str: the lastest note entry. If no notes exist, a default message is returned.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes found."

@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI summarize all current notes.

    :return: str: A prompt string that includes all notes and asks for a summary.
    If no notes exist, a message will be shown indicating that.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        content = f.read().strip()
    if not content:
        return "No notes found."
    return f"Summarize the current notes: {content}"

def main() -> None:
    pass


if __name__ == "__main__":
    main()