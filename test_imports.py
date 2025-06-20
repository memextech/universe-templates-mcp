#!/usr/bin/env python3
"""Test which imports are causing issues."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Testing imports...")

try:
    print("1. Testing asyncio...")
    import asyncio
    print("✓ asyncio imported successfully")
except Exception as e:
    print(f"✗ asyncio failed: {e}")

try:
    print("2. Testing MCP imports...")
    from mcp.server.models import InitializationOptions
    import mcp.types as types
    from mcp.server import NotificationOptions, Server
    print("✓ MCP imports successful")
except Exception as e:
    print(f"✗ MCP imports failed: {e}")

try:
    print("3. Testing requests...")
    import requests
    print("✓ requests imported successfully")
except Exception as e:
    print(f"✗ requests failed: {e}")

try:
    print("4. Testing pygit2...")
    import pygit2
    print("✓ pygit2 imported successfully")
except Exception as e:
    print(f"✗ pygit2 failed: {e}")

try:
    print("5. Testing firebase_admin...")
    import firebase_admin
    print("✓ firebase_admin imported successfully")
except Exception as e:
    print(f"✗ firebase_admin failed: {e}")

try:
    print("6. Testing our models...")
    from universe_templates.models import UniverseProject, TemplateDetails
    print("✓ models imported successfully")
except Exception as e:
    print(f"✗ models failed: {e}")

try:
    print("7. Testing firebase_client...")
    from universe_templates.firebase_client import FirebaseClient
    print("✓ firebase_client imported successfully")
except Exception as e:
    print(f"✗ firebase_client failed: {e}")

try:
    print("8. Testing git_utils...")
    from universe_templates.git_utils import clone_template_repository
    print("✓ git_utils imported successfully")
except Exception as e:
    print(f"✗ git_utils failed: {e}")

try:
    print("9. Testing server...")
    from universe_templates.server import main
    print("✓ server imported successfully")
except Exception as e:
    print(f"✗ server failed: {e}")

print("All imports tested!")