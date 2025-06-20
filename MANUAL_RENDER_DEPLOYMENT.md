# Manual Render Deployment Instructions

## Repository Successfully Created

✅ **GitHub Repository**: https://github.com/memextech/universe-templates-mcp
- Code successfully pushed to GitHub under memextech organization
- Repository is public and ready for deployment

## Deploy to Render (Manual Steps)

Since the Render CLI had some TTY issues, please follow these manual steps:

### Step 1: Access Render Dashboard
1. Go to [https://dashboard.render.com/](https://dashboard.render.com/)
2. Log in to your Render account

### Step 2: Create New Web Service
1. Click **"New +"** in the top right
2. Select **"Web Service"**
3. Choose **"Build and deploy from a Git repository"**

### Step 3: Connect Repository
1. Click **"Connect account"** if needed to connect your GitHub account
2. Search for and select: **memextech/universe-templates-mcp**
3. Click **"Connect"**

### Step 4: Configure Service Settings
Use these exact settings:

**Basic Settings:**
- **Name**: `universe-templates-mcp` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (uses repo root)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **Free** (or higher based on your needs)

### Step 5: Environment Variables (Optional)
No environment variables are required for basic operation. The server will use mock data if Firebase is not configured.

### Step 6: Deploy
1. Click **"Create Web Service"**
2. Render will automatically start building and deploying your service
3. Wait for the deployment to complete (usually 5-10 minutes)

## Expected Endpoints After Deployment

Once deployed, your service will be available at: `https://[your-service-name].onrender.com`

Test these endpoints:
- **Health Check**: `https://[your-service-name].onrender.com/health`
- **Service Info**: `https://[your-service-name].onrender.com/`
- **API Docs**: `https://[your-service-name].onrender.com/docs`
- **MCP SSE Endpoint**: `https://[your-service-name].onrender.com/sse`

## Alternative: Auto-Deploy with render.yaml

The repository includes a `render.yaml` file. If you want to use infrastructure-as-code:

1. In the Render Dashboard, look for the option to **"Deploy from render.yaml"**
2. Connect the GitHub repository
3. Render will automatically detect and use the `render.yaml` configuration

## Troubleshooting

If the deployment fails:
1. Check the build logs in the Render dashboard
2. Verify the Python version (should be 3.12+ for pygit2 compatibility)
3. Check that all dependencies install correctly

## Next Steps

After successful deployment:
1. Test all endpoints to ensure they're working
2. The MCP server will be accessible via SSE transport
3. You can connect MCP clients to the SSE endpoint
4. Use MCP proxies if you need stdio transport for local tools

## Repository Details

- **GitHub URL**: https://github.com/memextech/universe-templates-mcp
- **Organization**: memextech
- **Visibility**: Public
- **Latest Commit**: Includes all deployment files and documentation