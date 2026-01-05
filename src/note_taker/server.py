from mcp.server.fastmcp import FastMCP
import uuid
from typing import Dict, List
from smithery.decorators import smithery

# In-memory store
# Note: Data in this dict will persist while the server is running, 
# but will reset if the server restarts on Smithery.
NOTES: Dict[str, dict] = {}

@smithery.server()
def create_server():
    """Create and configure the Note Taker MCP server."""
    
    mcp = FastMCP("Note Taker MCP")

    @mcp.tool()
    def create_note(
        title: str,
        content: str,
        tags: List[str] = [],
    ) -> dict:
        """Create a new note with a title, content, and optional tags."""
        note_id = str(uuid.uuid4())
        NOTES[note_id] = {
            "note_id": note_id,
            "title": title,
            "content": content,
            "tags": tags,
        }
        return {
            "status": "created",
            "note_id": note_id,
        }

    @mcp.tool()
    def append_note(
        note_id: str,
        content: str,
    ) -> dict:
        """Append new text to the end of an existing note."""
        if note_id not in NOTES:
            return {"error": "Note not found"}

        NOTES[note_id]["content"] += "\n" + content
        return {
            "status": "updated",
            "note_id": note_id,
        }

    @mcp.tool()
    def get_note(note_id: str) -> dict:
        """Retrieve the full details of a specific note by its ID."""
        if note_id not in NOTES:
            return {"error": "Note not found"}
        return NOTES[note_id]

    @mcp.tool()
    def search_notes(query: str) -> list:
        """Search for notes containing the query string in title or content."""
        results = []
        for note in NOTES.values():
            if (
                query.lower() in note["title"].lower()
                or query.lower() in note["content"].lower()
            ):
                results.append(note)
        return results

    return mcp