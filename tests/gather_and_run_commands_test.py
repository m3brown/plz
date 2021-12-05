import pytest

from plz.runner import gather_and_run_commands

try:
    from mock import call, patch
except ImportError:
    from unittest.mock import call, patch


@patch("plz.runner.run_command")
def test_gather_and_run_string_cmd(mock_run):
    # Arrange
    mock_run.return_value = 0
    cmd = "test cmd"

    # Act
    gather_and_run_commands(cmd)

    # Assert
    mock_run.assert_called_with(cmd, cwd=None, args=[], env=None)


@patch("plz.runner.run_command")
def test_gather_and_run_return_value(mock_run):
    # Arrange
    mock_run.return_value = 0
    cmd = "test cmd"

    # Act
    rc = gather_and_run_commands(cmd)

    # Assert
    assert rc == 0


@patch("plz.runner.run_command")
def test_gather_and_run_list_cmds(mock_run):
    # Arrange
    mock_run.return_value = 0
    cmd = ["test cmd", "second cmd", "third cmd"]
    calls = [
        call(cmd[0], cwd=None, args=[], env=None),
        call(cmd[1], cwd=None, args=[], env=None),
        call(cmd[2], cwd=None, args=[], env=None),
    ]

    # Act
    gather_and_run_commands(cmd)

    # Assert
    mock_run.assert_has_calls(calls)


def test_gather_and_run_invalid_cmd():
    # Arrange
    cmd = 5

    # Act
    # Assert
    with pytest.raises(Exception):
        gather_and_run_commands(cmd)


@patch("plz.runner.run_command")
def test_gather_and_run_string_cmd_with_cwd(mock_run):
    # Arrange
    mock_run.return_value = 0
    cmd = "test cmd"

    # Act
    gather_and_run_commands(cmd, cwd="/root/path")

    # Assert
    mock_run.assert_called_with(cmd, cwd="/root/path", args=[], env=None)


@patch("plz.runner.run_command")
def test_gather_and_run_string_cmd_with_args(mock_run):
    # Arrange
    mock_run.return_value = 0
    cmd = "test cmd"
    args = ["derp", "herp"]

    # Act
    gather_and_run_commands(cmd, args=args)

    # Assert
    mock_run.assert_called_with(cmd, cwd=None, args=args, env=None)


@patch("plz.runner.run_command")
def test_gather_and_run_string_cmd_with_env(mock_run):
    # Arrange
    mock_run.return_value = 0
    cmd = "test cmd"
    args = ["derp", "herp"]
    env = {"foo": "bar"}

    # Act
    gather_and_run_commands(cmd, args=args, env=env)

    # Assert
    mock_run.assert_called_with(cmd, cwd=None, args=args, env=env)


@patch("plz.runner.run_command")
def test_gather_and_run_list_cmds_with_error(mock_run):
    # Arrange
    mock_run.return_value = 1
    cmd = ["test cmd", "second cmd", "third cmd"]
    calls = [
        call(cmd[0], cwd=None, args=[], env=None),
        call(cmd[1], cwd=None, args=[], env=None),
        call(cmd[2], cwd=None, args=[], env=None),
    ]

    # Act
    rc = gather_and_run_commands(cmd)

    # Assert
    assert rc == 1
    assert mock_run.call_count == 1
    mock_run.assert_called_once_with(cmd[0], cwd=None, args=[], env=None)
