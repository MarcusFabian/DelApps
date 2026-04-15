"""Unit tests for the main application module."""

from pathlib import Path
import sys


PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

import main as app_main


def test_greet_returns_default_message() -> None:
    """The default greeting should be returned when no name is provided."""
    assert app_main.greet() == "Hello, World!"


def test_greet_returns_personalized_message() -> None:
    """A personalized greeting should be returned when a name is provided."""
    assert app_main.greet("Marcus") == "Hello, Marcus!"