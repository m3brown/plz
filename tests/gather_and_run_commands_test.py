from plz.util import gather_and_run_commands
from mock import patch, call
import pytest


@patch('plz.util.run_command')
def test_gather_and_run_string_cmd(mock_run):
    # Arrange
    mock_run.return_value = (0, ['output'])
    cmd = "test cmd"

    # Act
    gather_and_run_commands(cmd)

    # Assert
    mock_run.assert_called_with(cmd)


@patch('plz.util.run_command')
def test_gather_and_run_list_cmds(mock_run):
    # Arrange
    mock_run.return_value = (0, ['output'])
    cmd = ["test cmd", "second cmd", "third cmd"]
    calls = map(call, cmd)

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
