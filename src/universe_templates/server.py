"""MCP Server for managing Memex universe templates."""

import asyncio
import json
import os
import logging
from typing import List, Dict, Any, Optional

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from .firebase_client import FirebaseClient, get_cached_projects, cache_projects, get_cached_project, cache_project
from .mock_data import get_mock_projects, get_mock_project_by_id, search_mock_projects
from .git_utils import clone_template_repository, get_directory_status, cleanup_failed_clone, GitError
from .models import TemplateDetails

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase client lazily
firebase_client = None

def get_firebase_client():
    global firebase_client
    if firebase_client is None:
        firebase_client = FirebaseClient()
    return firebase_client

server = Server("universe-templates")


def format_template_for_display(project: Dict[str, Any]) -> str:
    """Format a template project for display."""
    lines = [
        f"**{project.get('title', 'Untitled')}**",
        f"ID: {project.get('project_id', 'N/A')}",
        f"Description: {project.get('description', 'No description')}",
        f"Domain: {project.get('domain', 'N/A')}",
        f"Creator: {project.get('creator_id', 'N/A')}",
        f"Created: {project.get('created_at', 'N/A')}",
        f"Published: {'Yes' if project.get('is_published', False) else 'No'}",
    ]
    
    # Add features
    features = project.get('features', [])
    if features:
        lines.append(f"Features: {', '.join(features)}")
    
    # Add git info
    git_info = project.get('git')
    if git_info and git_info.get('url'):
        lines.append(f"Git Repository: {git_info['url']}")
        if git_info.get('branch'):
            lines.append(f"Branch: {git_info['branch']}")
    
    # Add deployment info
    deployment = project.get('deployment')
    if deployment and deployment.get('url'):
        lines.append(f"Live Demo: {deployment['url']}")
    
    return "\n".join(lines)


@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available template resources.
    Each template is exposed as a resource with a custom template:// URI scheme.
    """
    try:
        # Try to get cached projects first
        projects = get_cached_projects()
        if projects is None:
            # Try Firebase first, fall back to mock data
            client = get_firebase_client()
            projects = await client.list_universe_projects()
            if not projects:
                # Fall back to mock data if Firebase is unavailable
                projects = get_mock_projects()
                logger.info("Using mock data for templates")
            if projects:
                cache_projects(projects)
        
        resources = []
        for project in projects or []:
            if project.get('is_published', False):
                resources.append(
                    types.Resource(
                        uri=AnyUrl(f"template://universe/{project.get('project_id', '')}"),
                        name=f"Template: {project.get('title', 'Untitled')}",
                        description=project.get('description', 'No description'),
                        mimeType="text/plain",
                    )
                )
        
        logger.info(f"Listed {len(resources)} template resources")
        return resources
        
    except Exception as e:
        logger.error(f"Error listing resources: {e}")
        return []


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific template's details by its URI.
    """
    try:
        if uri.scheme != "template":
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

        # Extract project ID from URI path
        path = uri.path
        if path is not None:
            project_id = path.lstrip("/").split("/")[-1]  # Get the last part after splitting by "/"
        else:
            raise ValueError("No project ID in URI path")

        # Try to get from cache first
        project = get_cached_project(project_id)
        if project is None:
            # Try Firebase first, fall back to mock data
            client = get_firebase_client()
            project = await client.get_universe_project_details(project_id)
            if not project:
                # Fall back to mock data
                project = get_mock_project_by_id(project_id)
            if project:
                cache_project(project)
        
        if not project:
            raise ValueError(f"Template not found: {project_id}")
        
        return format_template_for_display(project)
        
    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        raise ValueError(f"Error reading template: {str(e)}")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools for managing universe templates.
    """
    return [
        types.Tool(
            name="list_universe_templates",
            description="List all available universe templates with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Filter by domain (e.g., 'AI', 'Web Development')"
                    },
                    "creator_id": {
                        "type": "string",
                        "description": "Filter by creator ID"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of templates to return",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="get_template_details",
            description="Get detailed information about a specific universe template",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "The unique ID of the template"
                    }
                },
                "required": ["template_id"]
            },
        ),
        types.Tool(
            name="search_templates",
            description="Search universe templates by keywords in title, description, or features",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (keywords to search for)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["query"]
            },
        ),
        types.Tool(
            name="clone_template",
            description="Clone a universe template repository to a local directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "The unique ID of the template to clone"
                    },
                    "target_directory": {
                        "type": "string",
                        "description": "The local directory path where the template should be cloned"
                    },
                    "project_name": {
                        "type": "string",
                        "description": "Optional project name (defaults to template title)"
                    }
                },
                "required": ["template_id", "target_directory"]
            },
        ),
        types.Tool(
            name="check_directory_status",
            description="Check the status of a directory (exists, empty, git repo, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to check"
                    }
                },
                "required": ["path"]
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests for universe templates.
    """
    try:
        if name == "list_universe_templates":
            return await handle_list_templates(arguments or {})
        elif name == "get_template_details":
            return await handle_get_template_details(arguments or {})
        elif name == "search_templates":
            return await handle_search_templates(arguments or {})
        elif name == "clone_template":
            return await handle_clone_template(arguments or {})
        elif name == "check_directory_status":
            return await handle_check_directory_status(arguments or {})
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error executing {name}: {str(e)}"
            )
        ]


async def handle_list_templates(arguments: dict) -> list[types.TextContent]:
    """Handle listing universe templates."""
    try:
        domain = arguments.get("domain")
        creator_id = arguments.get("creator_id")
        limit = arguments.get("limit", 20)
        
        # Try Firebase first, fall back to mock data
        client = get_firebase_client()
        projects = await client.list_universe_projects(creator_id=creator_id)
        if not projects:
            # Fall back to mock data
            projects = get_mock_projects()
            logger.info("Using mock data for listing templates")
        
        if not projects:
            return [
                types.TextContent(
                    type="text",
                    text="No universe templates found."
                )
            ]
        
        # Filter by domain if specified
        if domain:
            projects = [p for p in projects if p.get('domain', '').lower() == domain.lower()]
        
        # Filter published templates only
        projects = [p for p in projects if p.get('is_published', False)]
        
        # Simple sort by title for now to avoid comparison issues
        try:
            projects.sort(key=lambda x: x.get('title', ''), reverse=False)
        except Exception as e:
            logger.warning(f"Sorting failed: {e}, using unsorted list")
        
        # Apply limit
        projects = projects[:limit]
        
        # Cache the results
        cache_projects(projects)
        
        # Format output
        if len(projects) == 0:
            result_text = f"No templates found matching the criteria."
        else:
            result_lines = [f"Found {len(projects)} universe templates:\n"]
            
            for i, project in enumerate(projects, 1):
                result_lines.append(f"{i}. **{project.get('title', 'Untitled')}**")
                result_lines.append(f"   ID: {project.get('project_id', 'N/A')}")
                result_lines.append(f"   Description: {project.get('description', 'No description')}")
                result_lines.append(f"   Domain: {project.get('domain', 'N/A')}")
                result_lines.append(f"   Features: {', '.join(project.get('features', []))}")
                
                git_info = project.get('git')
                if git_info and git_info.get('url'):
                    result_lines.append(f"   Git: {git_info['url']}")
                
                result_lines.append("")  # Empty line between templates
            
            result_text = "\n".join(result_lines)
        
        return [
            types.TextContent(
                type="text",
                text=result_text
            )
        ]
        
    except Exception as e:
        logger.error(f"Error listing templates: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error listing templates: {str(e)}"
            )
        ]


async def handle_get_template_details(arguments: dict) -> list[types.TextContent]:
    """Handle getting detailed template information."""
    try:
        template_id = arguments.get("template_id")
        if not template_id:
            raise ValueError("template_id is required")
        
        # Try cache first
        project = get_cached_project(template_id)
        if project is None:
            # Try Firebase first, fall back to mock data
            client = get_firebase_client()
            project = await client.get_universe_project_details(template_id)
            if not project:
                # Fall back to mock data
                project = get_mock_project_by_id(template_id)
            if project:
                cache_project(project)
        
        if not project:
            return [
                types.TextContent(
                    type="text",
                    text=f"Template with ID '{template_id}' not found."
                )
            ]
        
        # Format detailed information
        details = format_template_for_display(project)
        
        # Add additional details
        details_lines = [details, "\n**Additional Details:**"]
        
        # Tools
        tools = project.get('tools', [])
        if tools:
            details_lines.append(f"Tools: {', '.join([t.get('name', 'Unknown') for t in tools])}")
        
        # Requirements
        requirements = project.get('requirements', [])
        if requirements:
            req_list = [f"{r.get('type', 'Unknown')}: {r.get('description', 'No description')}" for r in requirements]
            details_lines.append(f"Requirements:\n  - " + "\n  - ".join(req_list))
        
        # Pills (quick actions)
        pills = project.get('pills', [])
        if pills:
            pill_list = [f"{p.get('label', 'Unknown')}: {p.get('prompt', 'No prompt')}" for p in pills]
            details_lines.append(f"Quick Actions:\n  - " + "\n  - ".join(pill_list))
        
        result_text = "\n".join(details_lines)
        
        return [
            types.TextContent(
                type="text",
                text=result_text
            )
        ]
        
    except Exception as e:
        logger.error(f"Error getting template details: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error getting template details: {str(e)}"
            )
        ]


async def handle_search_templates(arguments: dict) -> list[types.TextContent]:
    """Handle searching universe templates."""
    try:
        query = arguments.get("query", "").lower()
        limit = arguments.get("limit", 20)
        
        if not query:
            raise ValueError("query is required")
        
        # Try Firebase first, fall back to mock data
        client = get_firebase_client()
        projects = await client.list_universe_projects()
        if not projects:
            # Fall back to mock data and search within it
            projects = search_mock_projects(query)
            logger.info("Using mock data for search")
        
        if not projects:
            return [
                types.TextContent(
                    type="text",
                    text="No universe templates available to search."
                )
            ]
        
        # Filter published templates only
        projects = [p for p in projects if p.get('is_published', False)]
        
        # Search in title, description, and features
        matching_projects = []
        for project in projects:
            title = project.get('title', '').lower()
            description = project.get('description', '').lower()
            features = ' '.join(project.get('features', [])).lower()
            domain = project.get('domain', '').lower()
            
            search_text = f"{title} {description} {features} {domain}"
            
            if query in search_text:
                # Calculate relevance score
                score = 0
                if query in title:
                    score += 10
                if query in description:
                    score += 5
                if query in features:
                    score += 3
                if query in domain:
                    score += 2
                
                matching_projects.append((score, project))
        
        # Sort by relevance score (descending)
        matching_projects.sort(key=lambda x: x[0], reverse=True)
        
        # Apply limit
        matching_projects = matching_projects[:limit]
        
        if len(matching_projects) == 0:
            result_text = f"No templates found matching '{query}'."
        else:
            result_lines = [f"Found {len(matching_projects)} templates matching '{query}':\n"]
            
            for i, (score, project) in enumerate(matching_projects, 1):
                result_lines.append(f"{i}. **{project.get('title', 'Untitled')}** (relevance: {score})")
                result_lines.append(f"   ID: {project.get('project_id', 'N/A')}")
                result_lines.append(f"   Description: {project.get('description', 'No description')}")
                result_lines.append(f"   Domain: {project.get('domain', 'N/A')}")
                result_lines.append(f"   Features: {', '.join(project.get('features', []))}")
                result_lines.append("")  # Empty line between templates
            
            result_text = "\n".join(result_lines)
        
        return [
            types.TextContent(
                type="text",
                text=result_text
            )
        ]
        
    except Exception as e:
        logger.error(f"Error searching templates: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error searching templates: {str(e)}"
            )
        ]


async def handle_clone_template(arguments: dict) -> list[types.TextContent]:
    """Handle cloning a universe template."""
    try:
        template_id = arguments.get("template_id")
        target_directory = arguments.get("target_directory")
        project_name = arguments.get("project_name")
        
        if not template_id:
            raise ValueError("template_id is required")
        if not target_directory:
            raise ValueError("target_directory is required")
        
        # Get template details
        project = get_cached_project(template_id)
        if project is None:
            client = get_firebase_client()
            project = await client.get_universe_project_details(template_id)
            if project:
                cache_project(project)
        
        if not project:
            return [
                types.TextContent(
                    type="text",
                    text=f"Template with ID '{template_id}' not found."
                )
            ]
        
        # Check if template has git repository
        git_info = project.get('git')
        if not git_info or not git_info.get('url'):
            return [
                types.TextContent(
                    type="text",
                    text=f"Template '{project.get('title', 'Unknown')}' does not have a git repository associated with it."
                )
            ]
        
        git_url = git_info['url']
        branch = git_info.get('branch', 'main')
        
        # Expand user home directory
        target_directory = os.path.expanduser(target_directory)
        
        # Check directory status before cloning
        dir_status = get_directory_status(target_directory)
        if dir_status['exists'] and not dir_status['is_empty']:
            return [
                types.TextContent(
                    type="text",
                    text=f"Target directory '{target_directory}' already exists and is not empty. Please choose a different location or remove the existing directory."
                )
            ]
        
        # Attempt to clone
        try:
            result = clone_template_repository(
                git_url=git_url,
                target_path=target_directory,
                project_name=project_name or project.get('title', 'Unknown'),
                branch=branch
            )
            
            # Format success message
            result_lines = [
                f"✅ Successfully cloned template '{project.get('title', 'Unknown')}'!",
                "",
                f"**Template Details:**",
                f"- Name: {project.get('title', 'Unknown')}",
                f"- Description: {project.get('description', 'No description')}",
                f"- Domain: {project.get('domain', 'N/A')}",
                "",
                f"**Clone Details:**",
                f"- Local Path: {result['path']}",
                f"- Git Repository: {result['remote_url']}",
                f"- Branch: {result['branch']}",
                f"- Latest Commit: {result['commit_id'][:8]}",
                f"- Commit Message: {result['commit_message']}",
                f"- Commit Author: {result['commit_author']}",
                "",
                f"**Next Steps:**",
                f"1. Navigate to the project directory: cd {result['path']}",
                f"2. Review the README.md file for setup instructions",
                f"3. Install any required dependencies",
                f"4. Start developing your project based on this template!"
            ]
            
            # Add template-specific next steps if available
            requirements = project.get('requirements', [])
            if requirements:
                result_lines.append("")
                result_lines.append("**Template Requirements:**")
                for req in requirements:
                    result_lines.append(f"- {req.get('type', 'Unknown')}: {req.get('description', 'No description')}")
            
            pills = project.get('pills', [])
            if pills:
                result_lines.append("")
                result_lines.append("**Quick Actions Available:**")
                for pill in pills:
                    result_lines.append(f"- {pill.get('label', 'Unknown')}: {pill.get('prompt', 'No prompt')}")
            
            return [
                types.TextContent(
                    type="text",
                    text="\n".join(result_lines)
                )
            ]
            
        except GitError as e:
            # Clean up failed clone attempt
            cleanup_failed_clone(target_directory)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"❌ Failed to clone template: {str(e)}\n\nPlease check that:\n- The git repository is accessible\n- You have proper permissions\n- The target directory path is valid"
                )
            ]
        
    except Exception as e:
        logger.error(f"Error cloning template: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error cloning template: {str(e)}"
            )
        ]


async def handle_check_directory_status(arguments: dict) -> list[types.TextContent]:
    """Handle checking directory status."""
    try:
        path = arguments.get("path")
        if not path:
            raise ValueError("path is required")
        
        # Expand user home directory
        path = os.path.expanduser(path)
        
        status = get_directory_status(path)
        
        result_lines = [
            f"**Directory Status: {path}**",
            "",
            f"Exists: {'Yes' if status['exists'] else 'No'}",
        ]
        
        if status['exists']:
            result_lines.extend([
                f"Is Directory: {'Yes' if status['is_directory'] else 'No'}",
                f"Is Empty: {'Yes' if status['is_empty'] else 'No'}",
                f"File Count: {status['file_count']}",
                f"Size: {status['size_bytes']:,} bytes",
                f"Is Git Repository: {'Yes' if status['is_git_repo'] else 'No'}",
            ])
            
            if not status['is_empty']:
                result_lines.append("")
                result_lines.append("⚠️  Directory is not empty. Cloning to this location may fail.")
        else:
            result_lines.append("")
            result_lines.append("✅ Directory does not exist. Safe to clone here.")
        
        return [
            types.TextContent(
                type="text",
                text="\n".join(result_lines)
            )
        ]
        
    except Exception as e:
        logger.error(f"Error checking directory status: {e}")
        return [
            types.TextContent(
                type="text",
                text=f"Error checking directory status: {str(e)}"
            )
        ]


async def main():
    """Main entry point for the MCP server."""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="universe-templates",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )