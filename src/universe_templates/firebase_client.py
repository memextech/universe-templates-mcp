"""Simple HTTP client for accessing public Firebase Function endpoints."""

import httpx
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class FirebaseClient:
    """HTTP client for accessing public Firebase Functions for universe projects."""
    
    def __init__(self, project_id: str = "memex-desktop", region: str = "us-central1"):
        self.project_id = project_id
        self.region = region
        self.base_url = f"https://{region}-{project_id}.cloudfunctions.net"
        
    async def list_universe_projects(self, creator_id: Optional[str] = None, title: Optional[str] = None) -> List[Dict[str, Any]]:
        """List universe projects from Firebase."""
        url = f"{self.base_url}/listUniverseProjects"
        
        payload = {"data": {}}
        if creator_id:
            payload["data"]["creator_id"] = creator_id
        if title:
            payload["data"]["title"] = title
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                
                result = response.json()
                if "result" in result:
                    return result["result"]
                else:
                    logger.warning(f"Unexpected response format: {result}")
                    return []
                    
        except httpx.HTTPError as e:
            logger.error(f"Error listing universe projects: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error listing universe projects: {e}")
            return []
    
    async def get_universe_project_details(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific universe project."""
        url = f"{self.base_url}/getUniverseProjectDetails"
        
        payload = {"data": {"project_id": project_id}}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                
                result = response.json()
                if "result" in result:
                    return result["result"]
                else:
                    logger.warning(f"Unexpected response format: {result}")
                    return None
                    
        except httpx.HTTPError as e:
            logger.error(f"Error getting project details for {project_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting project details for {project_id}: {e}")
            return None


# Simple in-memory cache for performance
_project_cache: Dict[str, Dict[str, Any]] = {}
_cache_timestamp: Optional[float] = None
CACHE_DURATION = 300  # 5 minutes

def get_cached_projects() -> Optional[List[Dict[str, Any]]]:
    """Get cached projects if still valid."""
    import time
    
    global _cache_timestamp, _project_cache
    
    if _cache_timestamp is None:
        return None
        
    if time.time() - _cache_timestamp > CACHE_DURATION:
        _project_cache.clear()
        _cache_timestamp = None
        return None
        
    return list(_project_cache.values())


def cache_projects(projects: List[Dict[str, Any]]):
    """Cache projects list."""
    import time
    
    global _cache_timestamp, _project_cache
    
    _project_cache.clear()
    for project in projects:
        _project_cache[project.get("project_id", "")] = project
    _cache_timestamp = time.time()


def get_cached_project(project_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific cached project."""
    return _project_cache.get(project_id)


def cache_project(project: Dict[str, Any]):
    """Cache a single project."""
    import time
    
    global _cache_timestamp
    
    project_id = project.get("project_id", "")
    if project_id:
        _project_cache[project_id] = project
        
    # Update cache timestamp if this is the first cached item
    if _cache_timestamp is None:
        _cache_timestamp = time.time()