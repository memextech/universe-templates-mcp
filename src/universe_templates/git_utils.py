"""Git utilities for cloning templates."""

import os
import shutil
import logging
from typing import Optional, Dict, Any
import pygit2

logger = logging.getLogger(__name__)


class GitError(Exception):
    """Custom exception for git operations."""
    pass


def clone_template_repository(
    git_url: str, 
    target_path: str, 
    project_name: Optional[str] = None,
    branch: str = "main"
) -> Dict[str, str]:
    """
    Clone a template repository to the target path.
    
    Args:
        git_url: Git repository URL
        target_path: Target directory path
        project_name: Optional project name (defaults to directory name)
        branch: Branch to checkout (defaults to main)
        
    Returns:
        Dict with status information
        
    Raises:
        GitError: If cloning fails
    """
    try:
        # Ensure target directory exists and is empty
        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                if os.listdir(target_path):
                    raise GitError(f"Target directory {target_path} already exists and is not empty")
            else:
                raise GitError(f"Target path {target_path} exists but is not a directory")
        else:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
        logger.info(f"Cloning repository from {git_url} to {target_path}")
        
        # Clone the repository
        repo = pygit2.clone_repository(git_url, target_path, checkout_branch=branch)
        
        # Remove original origin remote and add memex_universe remote
        if 'origin' in repo.remotes:
            repo.remotes.delete("origin")
            logger.info("Removed 'origin' remote")
            
        repo.remotes.create("memex_universe", git_url)
        logger.info(f"Added 'memex_universe' remote with URL {git_url}")
        
        # Get repository info
        head = repo.head
        commit = repo[head.target]
        
        result = {
            "status": "success",
            "path": target_path,
            "remote_url": git_url,
            "branch": branch,
            "commit_id": str(commit.id),
            "commit_message": commit.message.strip(),
            "commit_author": commit.author.name,
            "commit_date": commit.commit_time,
        }
        
        logger.info(f"Successfully cloned repository to {target_path}")
        return result
        
    except pygit2.GitError as e:
        error_msg = f"Git error while cloning {git_url}: {str(e)}"
        logger.error(error_msg)
        raise GitError(error_msg) from e
        
    except Exception as e:
        error_msg = f"Unexpected error while cloning {git_url}: {str(e)}"
        logger.error(error_msg)
        raise GitError(error_msg) from e


def validate_git_url(git_url: str) -> bool:
    """
    Validate if a git URL is accessible.
    
    Args:
        git_url: Git repository URL
        
    Returns:
        True if URL is valid and accessible
    """
    try:
        # Try to discover the repository
        pygit2.discover_repository(git_url)
        return True
    except:
        return False


def get_directory_status(path: str) -> Dict[str, Any]:
    """
    Get status information about a directory.
    
    Args:
        path: Directory path
        
    Returns:
        Dict with directory status information
    """
    result = {
        "exists": False,
        "is_directory": False,
        "is_empty": False,
        "is_git_repo": False,
        "file_count": 0,
        "size_bytes": 0
    }
    
    try:
        if os.path.exists(path):
            result["exists"] = True
            
            if os.path.isdir(path):
                result["is_directory"] = True
                
                # Check if empty
                contents = os.listdir(path)
                result["is_empty"] = len(contents) == 0
                result["file_count"] = len(contents)
                
                # Check if it's a git repository
                try:
                    pygit2.discover_repository(path)
                    result["is_git_repo"] = True
                except:
                    result["is_git_repo"] = False
                
                # Calculate directory size
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            total_size += os.path.getsize(filepath)
                        except OSError:
                            pass
                result["size_bytes"] = total_size
                
    except Exception as e:
        logger.error(f"Error getting directory status for {path}: {e}")
        
    return result


def cleanup_failed_clone(path: str) -> bool:
    """
    Clean up a failed clone attempt.
    
    Args:
        path: Directory path to clean up
        
    Returns:
        True if cleanup was successful
    """
    try:
        if os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)
            logger.info(f"Cleaned up failed clone at {path}")
            return True
    except Exception as e:
        logger.error(f"Error cleaning up failed clone at {path}: {e}")
        
    return False