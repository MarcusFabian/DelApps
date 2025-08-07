"""
Unit tests for the main module.
"""

import pytest
from src.main import greet


class TestGreet:
    """Test cases for the greet function."""
    
    def test_greet_with_name(self):
        """Test greeting with a specific name."""
        result = greet("Alice")
        assert result == "Hello, Alice!"
    
    def test_greet_without_name(self):
        """Test greeting without providing a name."""
        result = greet()
        assert result == "Hello, World!"
    
    def test_greet_with_empty_string(self):
        """Test greeting with an empty string."""
        result = greet("")
        assert result == "Hello, World!"
    
    def test_greet_with_none(self):
        """Test greeting with None explicitly."""
        result = greet(None)
        assert result == "Hello, World!"
