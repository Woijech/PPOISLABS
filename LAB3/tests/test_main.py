"""Tests for main.py entry point."""
from io import StringIO
import sys

from airport_system.main import main


def test_main_runs_successfully(capsys):
    """Test that main function runs without errors."""
    main()
    captured = capsys.readouterr()
    assert "Starting Airport System" in captured.out
    assert "Demo Airport" in captured.out
    assert "Scheduled flights:" in captured.out
