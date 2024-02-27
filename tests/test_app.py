"""
Module: test_app.py
This module contains unit tests for the App class.
"""

import multiprocessing  # Import the multiprocessing module
import pytest
from app import App

def test_app_get_environment_variable():
    """Function to test environment variable"""
    app = App()
    # Retrieve the current environment setting
    current_env = app.get_environment_variable('ENVIRONMENT')
    # Assert that the current environment is what you expect
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

def start_app(input_queue):
    """Function to start the App instance in a separate process."""
    app = App()
    app.command_handler.execute_command = lambda _: input_queue.get()  # Override execute_command to read from input_queue
    app.start()

def test_multiprocessing():
    """Test that the application runs in multiple processes."""
    input_queue = multiprocessing.Queue()

    process = multiprocessing.Process(target=start_app, args=(input_queue,))
    process.start()

    # Simulate user input by putting 'exit' into the input_queue
    input_queue.put('exit')

    process.join(timeout=2)

    assert not process.is_alive()


def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    app = App()
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    with pytest.raises(SystemExit) as exc_info:
        app.start()
    assert exc_info.type == SystemExit
    assert str(exc_info.value) == "Exiting..."

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    app = App()
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit) as exc_info:
        app.start()
    assert exc_info.type == SystemExit
    assert str(exc_info.value) == "Exiting..."
