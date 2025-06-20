# Deployment Guide for Universe Templates MCP Server

This guide explains how to deploy the Universe Templates MCP Server to Render.

## Overview

The MCP server has been wrapped with a FastAPI application that exposes the MCP functionality via Server-Sent Events (SSE) transport, making it deployable to cloud platforms like Render.

## Files Added for Deployment

- `app.py` - FastAPI wrapper with SSE support
- `requirements.txt` - Python dependencies for deployment
- `render.yaml` - Render service configuration
- `Dockerfile` - Container configuration (optional)

## Deployment to Render

### Method 1: Using Render Dashboard (Recommended)

1. **Prepare your repository:**
   - Ensure all deployment files are committed to your git repository
   - Push to GitHub, GitLab, or Bitbucket

2. **Create a new Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your repository

3. **Configure the service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3
   - **Plan:** Free (or higher based on needs)

4. **Environment Variables:**
   - The service should work without additional environment variables
   - If you need Firebase credentials, set them as environment variables

### Method 2: Using render.yaml

If you have a `render.yaml` file in your repository root, Render will automatically detect and use it for configuration.

### Method 3: Using Docker

The included `Dockerfile` can be used for containerized deployments:

```bash
docker build -t universe-templates-mcp .
docker run -p 8000:8000 universe-templates-mcp
```

## Testing the Deployment

Once deployed, your MCP server will be available at:
- **Health check:** `https://your-app.onrender.com/health`
- **SSE endpoint:** `https://your-app.onrender.com/sse`
- **API documentation:** `https://your-app.onrender.com/docs`

## Using the Deployed MCP Server

### With MCP Clients that support SSE

You can connect to your deployed server using the SSE endpoint:
```
https://your-app.onrender.com/sse
```

### Converting SSE to stdio for local use

If you need to use the deployed server with stdio-based MCP clients (like Claude Desktop), you can use an MCP proxy:

```bash
# Install mcp-proxy
npm install -g @modelcontextprotocol/inspector

# Connect to your deployed server
mcp-proxy https://your-app.onrender.com/sse
```

## Monitoring and Logs

- Use Render's dashboard to monitor your service
- Check logs via the Render dashboard or CLI
- The health endpoint can be used for uptime monitoring

## Limitations and Considerations

1. **Free tier limitations:** Render's free tier may have limitations on uptime and resources
2. **Cold starts:** The service may experience cold starts after periods of inactivity
3. **Persistent storage:** The service doesn't have persistent storage, so any local caching will be lost on restarts
4. **Environment variables:** Sensitive configuration should be set via Render's environment variables

## Troubleshooting

### Common Issues:

1. **Build failures:** Check that all dependencies in `requirements.txt` are correct
2. **Port binding:** Ensure the start command uses `$PORT` environment variable
3. **Import errors:** Verify that `PYTHONPATH` includes the source directory
4. **SSE connection issues:** Check that the SSE endpoint is accessible and not blocked by firewalls

### Debug Steps:

1. Check Render logs for error messages
2. Test the health endpoint first
3. Verify the SSE endpoint responds correctly
4. Use the MCP Inspector to test connections

## Security Considerations

- The service doesn't include authentication by default
- Consider adding authentication if deploying to production
- Environment variables should be used for sensitive configuration
- Regular security updates should be applied