from plz.runner import gather_and_run_commands
import pytest

try:
    from mock import patch, call
except ImportError:
    from unittest.mock import patch, call


@patch('plz.runner.run_command')
def test_gather_and_run_string_cmd(mock_run):
    # Arrange
    mock_run.return_value = (0, ['output'])
    cmd = "test cmd"

    # Act
    gather_and_run_commands(cmd)

    # Assert
    mock_run.assert_called_with(cmd, cwd=None, args=[])


@patch('plz.runner.run_command')
def test_gather_and_run_return_value(mock_run):
    # Arrange
    mock_run.return_value = (0, ['output'])
    cmd = "test cmd"

    # Act
    rc = gather_and_run_commands(cmd)

    # Assert
    assert rc == 0


@patch('plz.runner.run_command')
def test_gather_and_run_list_cmds(mock_run):
    # Arrange
    mock_run.return_value = (0, ['output'])
    cmd = ["test cmd", "second cmd", "third cmd"]
    calls = [
        call(cmd[0], cwd=None, args=[]),
        call(cmd[1], cwd=None, args=[]),
        call(cmd[2], cwd=None, args=[]),
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


@patch('plz.runner.run_command')
def test_gather_and_run_string_cmd_with_cwd(mock_run):
    # Arrange
    mock_run.return_value = (0, ['output'])
    cmd = "test cmd"

    # Act
    gather_and_run_commands(cmd, cwd="/root/path")

    # Assert
    mock_run.assert_called_with(cmd, cwd="/root/path", args=[])


@patch('plz.runner.run_command')
def test_gather_and_run_string_cmd_with_args(mock_run):
    # Arrange
    mock_run.return_value = (0, ['output'])
    cmd = "test cmd"
    args = ['derp', 'herp']

    # Act
    gather_and_run_commands(cmd, args=args)

    # Assert
    mock_run.assert_called_with(cmd, cwd=None, args=args)


@patch('plz.runner.run_command')
def test_gather_and_run_list_cmds_with_error(mock_run):
    # Arrange
    mock_run.return_value = (1, ['output'])
    cmd = ["test cmd", "second cmd", "third cmd"]
    calls = [
        call(cmd[0], cwd=None, args=[]),
        call(cmd[1], cwd=None, args=[]),
        call(cmd[2], cwd=None, args=[]),
    ]

    # Act
    rc = gather_and_run_commands(cmd)

    # Assert
    assert rc == 1
    assert mock_run.call_count == 1
    mock_run.assert_called_once_with(cmd[0], cwd=None, args=[])
