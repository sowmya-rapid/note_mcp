import uvicorn
from note_taker.server import create_server

# Create the server instance using your factory function
app = create_server()

if __name__ == "__main__":
    # Render provides a PORT environment variable we must use
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)