import pytest

from plz.runner import gather_and_run_commands, inject_shortcuts

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
    mock_run.assert_called_with(cmd)


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
        call(cmd[0]),
        call(cmd[1]),
        call(cmd[2]),
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
    mock_run.assert_called_with(cmd, cwd="/root/path")


@patch("plz.runner.run_command")
def test_gather_and_run_string_cmd_with_args(mock_run):
    # Arrange
    mock_run.return_value = 0
    cmd = "test cmd"
    args = ["derp", "herp"]

    # Act
    gather_and_run_commands(cmd, args=args)

    # Assert
    mock_run.assert_called_with(cmd, args=args)


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
    mock_run.assert_called_with(cmd, args=args, env=env)


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
    mock_run.assert_called_once_with(cmd[0])


@pytest.mark.parametrize(
    "cmd,shortcuts",
    [
        ["echo", {}],
        ["echo", {"foo": "bar"}],
        [["echo", "echo"], {}],
        [["echo", "echo"], {"foo": "bar"}],
    ],
)
@patch("plz.runner.inject_shortcuts")
def test_gather_and_run_calls_inject_shortcuts(mock_inject_shortcuts, cmd, shortcuts):
    # Arrange
    mock_inject_shortcuts.side_effect = lambda x, y: x
    if shortcuts:
        if type(cmd) == list:
            expected_calls = [call(command, shortcuts) for command in cmd]
        else:
            expected_calls = [call(cmd, shortcuts)]
    else:
        expected_calls = []

    # Act
    gather_and_run_commands(cmd, shortcuts=shortcuts)

    # Assert
    mock_inject_shortcuts.assert_has_calls(expected_calls)


@pytest.mark.parametrize(
    "command,shortcuts,expected_output",
    [
        ["test command", {}, "test command"],
        ["test command", {"foo": "bar"}, "test command"],
        ["test ${foo} command", {"foo": "bar"}, "test bar command"],
        ["test ${bar} command", {"foo": "bar"}, "test ${bar} command"],
        ["${foo} test command", {"foo": "bar"}, "bar test command"],
        ["test command ${foo}", {"foo": "bar"}, "test command bar"],
        [
            "test ${derp} command ${foo}",
            {"foo": "bar", "derp": "herp derp"},
            "test herp derp command bar",
        ],
        ['bash -c "${foo}"', {"foo": "bar"}, 'bash -c "bar"'],
    ],
)
def test_run_command_calls_inject_shortcuts(command, shortcuts, expected_output):
    # Arrange

    # Act
    result = inject_shortcuts(command, shortcuts)

    # Assert
    assert result == expected_output
