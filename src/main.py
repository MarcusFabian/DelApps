#!/usr/bin/env python3
"""
Main application entry point.

This is a simple Python application template.
You can modify this file to implement your specific functionality.
"""

import logging
from typing import Optional


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def greet(name: Optional[str] = None) -> str:
    """
    Generate a greeting message.
    
    Args:
        name: The name to greet. If None, uses a default greeting.
        
    Returns:
        A greeting message string.
    """
    if name:
        return f"Hello, {name}!"
    return "Hello, World!"


def main() -> None:
    """Main application function."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Python application")
    
    # Your application logic goes here
    message = greet("Python Developer")
    print(message)
    
    logger.info("Application completed successfully")


if __name__ == "__main__":
    main()
