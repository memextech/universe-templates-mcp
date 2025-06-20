"""Data models for universe templates."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


@dataclass
class Git:
    url: str
    branch: Optional[str] = None
    remote: Optional[str] = None


@dataclass
class Tool:
    name: str
    type: str
    version: Optional[str] = None
    role: Optional[str] = None


@dataclass
class Storage:
    gcs_path: Optional[str] = None
    size_bytes: Optional[int] = None
    last_sync: Optional[datetime] = None
    compression_enabled: Optional[bool] = None
    max_file_size_mb: Optional[int] = None


@dataclass
class Deployment:
    url: str
    type: Optional[str] = None
    last_deployed: Optional[datetime] = None


@dataclass
class Requirement:
    type: str
    description: str


@dataclass
class Pill:
    label: str
    prompt: str
    icon: Optional[str] = None


@dataclass
class UniverseProject:
    project_id: str
    title: str
    description: str
    slug: str
    domain: str
    creator_id: str
    created_at: datetime
    updated_at: datetime
    is_published: bool
    published_at: Optional[datetime] = None
    features: List[str] = None
    requirements: List[Requirement] = None
    tools: List[Tool] = None
    icon: Optional[str] = None
    card_image: Optional[str] = None
    hero_image: Optional[str] = None
    git: Optional[Git] = None
    storage: Optional[Storage] = None
    deployment: Optional[Deployment] = None
    getting_started_screen: bool = False
    getting_started_screen_index: Optional[int] = None
    pills: Optional[List[Pill]] = None

    def __post_init__(self):
        if self.features is None:
            self.features = []
        if self.requirements is None:
            self.requirements = []
        if self.tools is None:
            self.tools = []
        if self.pills is None:
            self.pills = []


# Pydantic models for API requests
class ListTemplatesRequest(BaseModel):
    domain: Optional[str] = None
    creator_id: Optional[str] = None
    features: Optional[List[str]] = None
    limit: Optional[int] = 20
    offset: Optional[int] = 0


class SearchTemplatesRequest(BaseModel):
    query: str
    limit: Optional[int] = 20
    offset: Optional[int] = 0


class CloneTemplateRequest(BaseModel):
    template_id: str
    target_directory: str
    project_name: Optional[str] = None


class TemplateDetails(BaseModel):
    """Simplified template details for API responses."""
    project_id: str
    title: str
    description: str
    domain: str
    creator_id: str
    created_at: str
    updated_at: str
    is_published: bool
    features: List[str] = []
    tools: List[Dict[str, Any]] = []
    requirements: List[Dict[str, str]] = []
    icon: Optional[str] = None
    card_image: Optional[str] = None
    hero_image: Optional[str] = None
    git: Optional[Dict[str, str]] = None
    deployment: Optional[Dict[str, str]] = None
    getting_started_screen: bool = False
    getting_started_screen_index: Optional[int] = None
    pills: List[Dict[str, str]] = []