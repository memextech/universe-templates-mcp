"""FastAPI web server wrapper for the MCP Universe Templates server.

This provides an HTTP/SSE interface to the MCP server for deployment to cloud platforms like Render.
"""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import Response

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
from mcp.server.sse import SseServerTransport

# Import the MCP server instance
from src.universe_templates.server import server

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager."""
    logger.info("Starting Universe Templates MCP Server")
    yield
    logger.info("Shutting down Universe Templates MCP Server")


# Create FastAPI app
app = FastAPI(
    title="Universe Templates MCP Server",
    description="MCP server for managing Memex universe templates - HTTP/SSE interface",
    version="0.1.0",
    lifespan=lifespan
)

# Create SSE transport
sse_transport = SseServerTransport("/messages/")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Universe Templates MCP Server",
        "version": "0.1.0",
        "transport": "SSE",
        "endpoints": {
            "sse": "/sse",
            "messages": "/messages",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "server": "universe-templates"}


async def handle_sse(request: Request):
    """Handle SSE connections for MCP communication."""
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0], streams[1],
            InitializationOptions(
                server_name="universe-templates",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
    # Return empty response to avoid NoneType error
    return Response()


# Create Starlette app for SSE handling
sse_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse, methods=["GET"]),
        Mount("/messages/", app=sse_transport.handle_post_message),
    ]
)

# Mount the SSE app
app.mount("/", sse_app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)