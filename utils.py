"""
Utility functions for the research assistant.
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Union
from functools import wraps
import time
from config import APP_CONFIG, TASK_CONFIG, ERROR_MESSAGES, CACHE_DIR

logger = logging.getLogger(__name__)

class OutputValidator:
    """Validate and format agent outputs."""

    @staticmethod
    def validate_research_output(output: str) -> Dict[str, Any]:
        """Validate research output format."""
        try:
            # Extract findings and sources from markdown format
            sections = output.split("##")
            findings = sections[0].strip()
            sources = sections[1].strip() if len(sections) > 1 else ""

            # Validate required fields
            if not findings or not sources:
                raise ValueError("Missing required sections")

            return {
                "findings": findings,
                "sources": sources,
                "valid": True
            }
        except Exception as e:
            logger.error(f"Research output validation failed: {e}")
            return {"valid": False, "error": str(e)}

    @staticmethod
    def validate_writing_output(output: str) -> Dict[str, Any]:
        """Validate writing output format."""
        try:
            # Split content and sources
            parts = output.split("---")
            content = parts[0].strip()
            sources = parts[1].strip() if len(parts) > 1 else ""

            # Validate word count
            word_count = len(content.split())
            if not (TASK_CONFIG["writing"]["min_words"] <= word_count <= TASK_CONFIG["writing"]["max_words"]):
                raise ValueError(f"Word count {word_count} outside allowed range")

            return {
                "content": content,
                "sources": sources,
                "valid": True,
                "word_count": word_count
            }
        except Exception as e:
            logger.error(f"Writing output validation failed: {e}")
            return {"valid": False, "error": str(e)}

class CacheManager:
    """Manage result caching."""

    @staticmethod
    def get_cache_key(query: str) -> str:
        """Generate cache key from query."""
        return hashlib.md5(query.encode()).hexdigest()

    @staticmethod
    def get_cached_result(query: str) -> Optional[str]:
        """Get cached result for query."""
        if not APP_CONFIG["CACHE_ENABLED"]:
            return None

        cache_key = CacheManager.get_cache_key(query)
        cache_file = CACHE_DIR / f"{cache_key}.json"

        try:
            if cache_file.exists():
                data = json.loads(cache_file.read_text())
                if time.time() - data["timestamp"] < APP_CONFIG["CACHE_TTL"]:
                    logger.debug(f"Cache hit for query: {query}")
                    return data["result"]
        except Exception as e:
            logger.error(f"Cache read error: {e}")

        return None

    @staticmethod
    def cache_result(query: str, result: str) -> None:
        """Cache result for query."""
        if not APP_CONFIG["CACHE_ENABLED"]:
            return

        cache_key = CacheManager.get_cache_key(query)
        cache_file = CACHE_DIR / f"{cache_key}.json"

        try:
            data = {
                "query": query,
                "result": result,
                "timestamp": time.time()
            }
            cache_file.write_text(json.dumps(data))
            logger.debug(f"Cached result for query: {query}")
        except Exception as e:
            logger.error(f"Cache write error: {e}")

def retry_on_error(max_retries: int = APP_CONFIG["MAX_RETRIES"], delay: int = 1):
    """Decorator to retry functions on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
            return None
        return wrapper
    return decorator

def sanitize_query(query: str) -> str:
    """Sanitize user input query."""
    # Remove potentially harmful characters
    query = "".join(c for c in query if c.isprintable())
    # Truncate to maximum length
    return query[:APP_CONFIG["MAX_QUERY_LENGTH"]]

def format_error(error_key: str, *args) -> str:
    """Format error message from config."""
    try:
        return ERROR_MESSAGES[error_key].format(*args)
    except KeyError:
        return f"Unknown error: {error_key}"
    except Exception as e:
        return f"Error formatting message: {str(e)}"
