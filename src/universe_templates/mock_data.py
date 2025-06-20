"""Mock data for testing the MCP server without Firebase dependencies."""

from typing import List, Dict, Any
import datetime

# Mock universe project data
MOCK_UNIVERSE_PROJECTS: List[Dict[str, Any]] = [
    {
        "project_id": "nextjs-ai-chat",
        "title": "Next.js AI Chat Template",
        "description": "A modern chat application template built with Next.js, TypeScript, and AI integration. Features real-time messaging, user authentication, and AI-powered responses.",
        "slug": "nextjs-ai-chat",
        "domain": "Web Development",
        "creator_id": "user-123",
        "created_at": "2024-12-01T10:00:00Z",
        "updated_at": "2024-12-01T10:00:00Z",
        "is_published": True,
        "published_at": "2024-12-01T10:00:00Z",
        "features": ["Next.js", "TypeScript", "AI Integration", "Real-time Chat", "Authentication"],
        "requirements": [
            {"type": "Node.js", "description": "Version 18 or higher"},
            {"type": "Database", "description": "PostgreSQL or similar"},
            {"type": "API Key", "description": "OpenAI API key for AI features"}
        ],
        "tools": [
            {"name": "Next.js", "type": "framework", "version": "14.0", "role": "Frontend framework"},
            {"name": "TypeScript", "type": "language", "version": "5.0", "role": "Type safety"},
            {"name": "Prisma", "type": "orm", "version": "5.0", "role": "Database ORM"}
        ],
        "icon": "💬",
        "card_image": "https://example.com/chat-app-preview.png",
        "hero_image": "https://example.com/chat-app-hero.png",
        "git": {
            "url": "https://github.com/memex-universe/nextjs-ai-chat-template.git",
            "branch": "main",
            "remote": "memex_universe"
        },
        "storage": {
            "gcs_path": "universe-templates/nextjs-ai-chat",
            "size_bytes": 1024000,
            "compression_enabled": True
        },
        "deployment": {
            "url": "https://nextjs-ai-chat-demo.vercel.app",
            "type": "vercel",
            "last_deployed": "2024-12-01T10:00:00Z"
        },
        "getting_started_screen": True,
        "getting_started_screen_index": 1,
        "pills": [
            {"label": "Quick Start", "prompt": "Set up the basic chat functionality", "icon": "🚀"},
            {"label": "Add AI", "prompt": "Integrate AI responses to the chat", "icon": "🤖"},
            {"label": "Deploy", "prompt": "Deploy to Vercel", "icon": "🌐"}
        ]
    },
    {
        "project_id": "python-fastapi-starter",
        "title": "Python FastAPI Starter",
        "description": "A robust FastAPI starter template with authentication, database integration, testing, and Docker support. Perfect for building modern APIs quickly.",
        "slug": "python-fastapi-starter",
        "domain": "Backend Development",
        "creator_id": "user-456",
        "created_at": "2024-11-15T14:30:00Z",
        "updated_at": "2024-11-20T09:15:00Z",
        "is_published": True,
        "published_at": "2024-11-15T14:30:00Z",
        "features": ["FastAPI", "SQLAlchemy", "JWT Auth", "Docker", "Testing", "API Documentation"],
        "requirements": [
            {"type": "Python", "description": "Version 3.11 or higher"},
            {"type": "Database", "description": "PostgreSQL recommended"},
            {"type": "Docker", "description": "For containerized deployment"}
        ],
        "tools": [
            {"name": "FastAPI", "type": "framework", "version": "0.104", "role": "API framework"},
            {"name": "SQLAlchemy", "type": "orm", "version": "2.0", "role": "Database ORM"},
            {"name": "Pytest", "type": "testing", "version": "7.4", "role": "Testing framework"}
        ],
        "icon": "⚡",
        "card_image": "https://example.com/fastapi-preview.png",
        "hero_image": "https://example.com/fastapi-hero.png",
        "git": {
            "url": "https://github.com/memex-universe/python-fastapi-starter.git",
            "branch": "main",
            "remote": "memex_universe"
        },
        "deployment": {
            "url": "https://fastapi-starter-demo.railway.app",
            "type": "railway",
            "last_deployed": "2024-11-20T09:15:00Z"
        },
        "getting_started_screen": True,
        "getting_started_screen_index": 2,
        "pills": [
            {"label": "Setup Environment", "prompt": "Set up the development environment with poetry", "icon": "🐍"},
            {"label": "Database Setup", "prompt": "Configure and run database migrations", "icon": "🗄️"},
            {"label": "Add Endpoints", "prompt": "Create your first API endpoints", "icon": "🔗"}
        ]
    },
    {
        "project_id": "react-dashboard",
        "title": "React Dashboard Template",
        "description": "A comprehensive dashboard template built with React, featuring charts, tables, user management, and responsive design. Includes dark mode and theming.",
        "slug": "react-dashboard",
        "domain": "Frontend Development",
        "creator_id": "user-789",
        "created_at": "2024-10-20T16:45:00Z",
        "updated_at": "2024-11-25T11:20:00Z",
        "is_published": True,
        "published_at": "2024-10-20T16:45:00Z",
        "features": ["React", "Charts", "Tables", "Dark Mode", "Responsive", "User Management"],
        "requirements": [
            {"type": "Node.js", "description": "Version 18 or higher"},
            {"type": "Package Manager", "description": "npm or yarn"}
        ],
        "tools": [
            {"name": "React", "type": "library", "version": "18.2", "role": "UI library"},
            {"name": "Material-UI", "type": "ui-library", "version": "5.14", "role": "Component library"},
            {"name": "Chart.js", "type": "visualization", "version": "4.4", "role": "Data visualization"}
        ],
        "icon": "📊",
        "card_image": "https://example.com/dashboard-preview.png",
        "hero_image": "https://example.com/dashboard-hero.png",
        "git": {
            "url": "https://github.com/memex-universe/react-dashboard-template.git",
            "branch": "main",
            "remote": "memex_universe"
        },
        "deployment": {
            "url": "https://react-dashboard-demo.netlify.app",
            "type": "netlify",
            "last_deployed": "2024-11-25T11:20:00Z"
        },
        "getting_started_screen": False,
        "pills": [
            {"label": "Customize Theme", "prompt": "Customize colors and branding", "icon": "🎨"},
            {"label": "Add Charts", "prompt": "Create new chart components", "icon": "📈"},
            {"label": "User System", "prompt": "Set up user authentication and roles", "icon": "👥"}
        ]
    },
    {
        "project_id": "ml-model-serving",
        "title": "ML Model Serving API",
        "description": "A production-ready template for serving machine learning models via REST API. Includes model versioning, monitoring, and scalable deployment.",
        "slug": "ml-model-serving",
        "domain": "Machine Learning",
        "creator_id": "user-101",
        "created_at": "2024-09-10T08:00:00Z",
        "updated_at": "2024-12-01T15:30:00Z",
        "is_published": True,
        "published_at": "2024-09-10T08:00:00Z",
        "features": ["FastAPI", "MLflow", "Docker", "Model Versioning", "Monitoring", "Async Processing"],
        "requirements": [
            {"type": "Python", "description": "Version 3.9 or higher"},
            {"type": "GPU", "description": "Optional but recommended for deep learning models"},
            {"type": "Storage", "description": "Model storage solution (S3, GCS, etc.)"}
        ],
        "tools": [
            {"name": "FastAPI", "type": "framework", "version": "0.104", "role": "API framework"},
            {"name": "MLflow", "type": "ml-platform", "version": "2.8", "role": "Model tracking"},
            {"name": "Prometheus", "type": "monitoring", "version": "latest", "role": "Metrics collection"}
        ],
        "icon": "🤖",
        "card_image": "https://example.com/ml-api-preview.png",
        "git": {
            "url": "https://github.com/memex-universe/ml-model-serving-template.git",
            "branch": "main",
            "remote": "memex_universe"
        },
        "deployment": {
            "url": "https://ml-api-demo.herokuapp.com",
            "type": "heroku",
            "last_deployed": "2024-12-01T15:30:00Z"
        },
        "getting_started_screen": True,
        "getting_started_screen_index": 3,
        "pills": [
            {"label": "Load Model", "prompt": "Load and configure your ML model", "icon": "🧠"},
            {"label": "API Endpoints", "prompt": "Set up prediction endpoints", "icon": "🔌"},
            {"label": "Deploy Scale", "prompt": "Deploy with auto-scaling", "icon": "📈"}
        ]
    }
]


def get_mock_projects() -> List[Dict[str, Any]]:
    """Return mock universe projects."""
    return MOCK_UNIVERSE_PROJECTS


def get_mock_project_by_id(project_id: str) -> Dict[str, Any] | None:
    """Get a specific mock project by ID."""
    for project in MOCK_UNIVERSE_PROJECTS:
        if project["project_id"] == project_id:
            return project
    return None


def search_mock_projects(query: str) -> List[Dict[str, Any]]:
    """Search mock projects by query."""
    query = query.lower()
    results = []
    
    for project in MOCK_UNIVERSE_PROJECTS:
        # Search in title, description, features, and domain
        search_text = (
            project.get("title", "").lower() + " " +
            project.get("description", "").lower() + " " +
            " ".join(project.get("features", [])).lower() + " " +
            project.get("domain", "").lower()
        )
        
        if query in search_text:
            results.append(project)
    
    return results