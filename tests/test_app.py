"""
Module: test_app.py
This module contains unit tests for the App class.
"""

import multiprocessing
import pytest
from app import App

def test_app_get_environment_variable():
    """Function to test enviroment variable"""
    app = App()
#   Retrieve the current environment setting
    current_env = app.get_environment_variable('ENVIRONMENT')
    # Assert that the current environment is what you expect
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

"""
Module-level docstring: This module contains tests for the App class.
"""

from app import App

def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    App.start()
    out, _ = capfd.readouterr()

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    App.start()
    out, _ = capfd.readouterr()

    app = App()

    with pytest.raises(SystemExit):
        app.start()

    captured = capfd.readouterr()
    assert "No such command: unknown_command" in captured.out


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
