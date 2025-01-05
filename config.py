"""
Application configuration settings.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Base paths
BASE_DIR = Path(__file__).parent
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"

# Ensure directories exist
CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Application settings
APP_CONFIG: Dict[str, Any] = {
    # Timeouts
    "TASK_TIMEOUT": 300,  # 5 minutes
    "QUERY_TIMEOUT": 600,  # 10 minutes
    "CONNECTION_TIMEOUT": 30,  # 30 seconds

    # Output formatting
    "PAGE_SIZE": 20,
    "MAX_QUERY_LENGTH": 500,
    "MAX_RETRIES": 3,

    # Logging
    "LOG_LEVEL": "DEBUG",
    "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "LOG_FILE": LOG_DIR / "app.log",
    "MAX_LOG_SIZE": 10 * 1024 * 1024,  # 10MB
    "LOG_BACKUP_COUNT": 5,

    # Cache settings
    "CACHE_ENABLED": True,
    "CACHE_TTL": 3600,  # 1 hour
    "MAX_CACHE_SIZE": 100 * 1024 * 1024,  # 100MB

    # Output formats
    "RESEARCH_FORMAT": """
    # Research Findings

    {findings}

    ## Sources
    {sources}
    """,

    "WRITING_FORMAT": """
    {content}

    ---
    Sources:
    {sources}
    """,
}

# Task-specific settings
TASK_CONFIG = {
    "research": {
        "max_sources": 5,
        "min_confidence": 0.7,
        "required_fields": ["finding", "source", "confidence"],
    },
    "writing": {
        "max_paragraphs": 3,
        "min_words": 100,
        "max_words": 500,
        "required_fields": ["content", "sources"],
    }
}

# Error messages
ERROR_MESSAGES = {
    "timeout": "The operation timed out. Please try again.",
    "invalid_query": "Please enter a valid query (max {} characters).",
    "no_results": "No results found. Please try a different query.",
    "task_failed": "Task failed: {}. Retrying... ({}/{})",
    "connection_error": "Connection error. Please check your internet connection.",
    "validation_error": "Invalid output format: {}",
}
