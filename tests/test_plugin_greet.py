"""
Module: test_plugin_greet.py
This module contains unit tests for the 'greet' command in the App class.
"""

import pytest
from app import App

def test_app_greet_command(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'greet' command and outputs 'Hello, World!'."""
    inputs = iter(['greet', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()

    # Check that the exit was graceful with the correct exit code
    assert e.value.code == 0, "The app did not exit as expected"

    # Capture the output from the 'greet' command
    out, _ = capfd.readouterr()

    # Assert that 'Hello, World!' was printed to stdout
    assert "Hello, World!" in out, "The 'greet' command did not produce the expected output."
