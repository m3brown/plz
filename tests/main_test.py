import sys
import textwrap
from unittest.mock import ANY, patch

import pytest

from plz import main


def get_sample_config(**overrides):
    return {"commands": {"testcmd": {"cmd": "derp", **overrides}}}


@patch("sys.exit")
@patch("plz.main.plz_config")
@patch("plz.main.list_options")
def test_main_with_no_argument_call_list_options(mock_list, mock_config, mock_exit):
    # Arrange
    config = get_sample_config()
    mock_config.return_value = (config, None)
    # Act
    main.main([])
    # Assert
    mock_list.assert_called_with(config)


@patch("sys.exit")
@patch("plz.main.plz_config")
@patch("plz.main.list_options")
def test_main_with_help_argument_call_list_options(mock_list, mock_config, mock_exit):
    # Arrange
    config = get_sample_config()
    mock_config.return_value = (config, None)
    # Act
    main.main(["help"])
    # Assert
    mock_list.assert_called_with(config)


@patch("sys.exit")
@patch("plz.main.plz_config")
@patch("plz.main.command_detail")
def test_main_with_help_argument_and_command_name_calls_command_detail(
    mock_detail, mock_config, mock_exit
):
    # Arrange
    config = get_sample_config()
    mock_config.return_value = (config, None)
    # Act
    main.main(["help", "testcmd"])
    # Assert
    mock_detail.assert_called_with("testcmd", config["commands"]["testcmd"])


@patch("sys.exit")
@patch("plz.main.plz_config")
@patch("plz.main.list_options")
@patch("plz.main.command_detail")
def test_main_with_help_argument_and_bad_command_name_calls_list_options(
    mock_detail, mock_list_options, mock_config, mock_exit
):
    # Arrange
    config = get_sample_config()
    mock_config.return_value = (config, None)
    # Act
    main.main(["help", "foo"])
    # Assert
    mock_detail.assert_not_called()
    mock_list_options.assert_called_with(config)


@patch.object(sys, "argv", ["/root/path/plz", "testcmd", "arg1", "arg2"])
@patch("plz.main.execute_from_config")
def test_main_with_sys_argv_parsing(mock_execute):
    # Arrange
    # Act
    main.main()

    # Assert
    mock_execute.assert_called_with("testcmd", ["arg1", "arg2"])


@patch("plz.main.execute_from_config")
def test_main_with_single_argument(mock_execute):
    # Arrange
    # Act
    main.main(["testcmd"])

    # Assert
    mock_execute.assert_called_with("testcmd", [])


@patch("plz.main.execute_from_config")
def test_main_with_passthrough_argument(mock_execute):
    # Arrange
    # Act
    main.main(["testcmd", "arg1"])

    # Assert
    mock_execute.assert_called_with("testcmd", ["arg1"])


@patch("plz.main.execute_from_config")
def test_main_with_several_passthrough_arguments(mock_execute):
    # Arrange
    # Act
    main.main(["testcmd", "arg1", "arg2", "arg3"])

    # Assert
    mock_execute.assert_called_with("testcmd", ["arg1", "arg2", "arg3"])


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_with_valid_cmd(mock_plz_config, mock_gather, mock_exit):
    # Arrange
    args = ["args"]
    config = get_sample_config()
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with("derp", cwd=None, args=args, shortcuts={})


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_handles_string_command(
    mock_plz_config, mock_gather, mock_exit
):
    # Arrange
    args = ["args"]
    config = get_sample_config()
    config["commands"]["testcmd"] = "test string"
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with("test string", cwd=None, args=args, shortcuts={})


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_handles_list_command(
    mock_plz_config, mock_gather, mock_exit
):
    # Arrange
    args = ["args"]
    config = get_sample_config()
    list_command = ["test string", "another string"]
    config["commands"]["testcmd"] = list_command
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with(list_command, cwd=None, args=args, shortcuts={})


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_with_dir(mock_plz_config, mock_gather, mock_exit):
    # Arrange
    args = ["args"]
    config = get_sample_config(dir="foo")
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with("derp", cwd="foo", args=args, shortcuts={})


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_with_valid_cmd_and_cwd(
    mock_plz_config, mock_gather, mock_exit
):
    # Arrange
    args = ["args"]
    cwd = "/root/path"
    config = get_sample_config()
    mock_plz_config.return_value = (config, cwd)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with("derp", cwd=cwd, args=args, shortcuts={})


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_with_cwd_and_dir(mock_plz_config, mock_gather, mock_exit):
    # Arrange
    args = ["args"]
    cwd = "/root/path"
    config = get_sample_config(dir="foo")
    mock_plz_config.return_value = (
        config,
        cwd,
    )

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with(
        "derp", cwd="/root/path/foo", args=args, shortcuts={}
    )


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
@patch("plz.main.compile_environment")
def test_execute_from_config_passes_env_dict_if_defined(
    mock_compile_environment, mock_plz_config, mock_gather, mock_exit
):
    # Arrange
    args = ["args"]
    config = get_sample_config()
    mock_plz_config.return_value = (config, None)
    mock_compile_environment.return_value = {"foo": "bar"}

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with(
        ANY, cwd=ANY, args=ANY, env={"foo": "bar"}, shortcuts=ANY
    )


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_passes_shortcuts_dict_if_defined(
    mock_plz_config, mock_gather, mock_exit
):
    # Arrange
    args = ["args"]
    shortcuts = {"foo": "bar"}
    config = get_sample_config()
    config["shortcuts"] = shortcuts
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with(ANY, cwd=ANY, args=ANY, shortcuts=shortcuts)


@patch("sys.exit")
@patch("plz.main.plz_config")
def test_execute_from_config_with_invalid_cmd(mock_plz_config, mock_exit):
    # Arrange
    args = ["args"]
    config = get_sample_config()
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("badcmd", args)

    # Assert
    mock_exit.assert_called_with(1)


@patch("sys.exit")
@patch("plz.main.plz_config")
def test_execute_from_config_with_valid_cmd_with_no_inner_cmd(
    mock_plz_config, mock_exit
):
    # Arrange
    args = ["args"]
    config = get_sample_config()
    cmd = config["commands"]["testcmd"]
    cmd["noncmd"] = cmd.pop("cmd")
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_exit.assert_called_with(1)


@patch("sys.exit")
@patch("plz.main.gather_and_run_commands")
@patch("plz.main.plz_config")
def test_execute_from_config_with_complex_cmd(mock_plz_config, mock_gather, mock_exit):
    # Arrange
    args = ["args"]
    config = get_sample_config(cmd=["derp", "herp"])
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("testcmd", args)

    # Assert
    mock_gather.assert_called_with(["derp", "herp"], cwd=None, args=args, shortcuts={})


@patch("sys.exit")
@patch("plz.main.list_options")
@patch("plz.main.plz_config")
def test_execute_from_config_with_invalid_cmd_calls_list_options(
    mock_plz_config, mock_list, mock_exit
):
    # Arrange
    args = ["args"]
    config = get_sample_config()
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("badcmd", args)

    # Assert
    mock_list.assert_called_with(mock_plz_config.return_value[0])


@patch("sys.exit")
@patch("plz.main.plz_config")
def test_execute_from_config_prints_info_to_stdout(mock_plz_config, mock_exit, capfd):
    # Arrange
    config = {"commands": {"foo": {"cmd": "echo bar"}}}
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("foo", [])
    out, err = capfd.readouterr()

    # Assert
    assert (
        out
        == textwrap.dedent(
            """
        \x1b[36m\x1b[2m
        ===============================================================================
        Running command: echo bar
        ===============================================================================
        \x1b[0m
        bar

        \x1b[36m\x1b[2m[INFO] Process complete\x1b[0m
        """
        ).lstrip()
    )


@patch("sys.exit")
@patch("plz.main.plz_config")
def test_execute_from_config_prints_description_if_defined(
    mock_plz_config, mock_exit, capfd
):
    # Arrange
    config = {"commands": {"foo": {"cmd": "echo bar", "description": "a description"}}}
    mock_plz_config.return_value = (config, None)

    # Act
    main.execute_from_config("foo", [])
    out, err = capfd.readouterr()

    # Assert
    assert (
        out
        == textwrap.dedent(
            """
        \x1b[36m
        Description: a description\x1b[0m
        \x1b[36m\x1b[2m
        ===============================================================================
        Running command: echo bar
        ===============================================================================
        \x1b[0m
        bar

        \x1b[36m\x1b[2m[INFO] Process complete\x1b[0m
        """
        ).lstrip()
    )


@pytest.mark.parametrize(
    "os_environ,global_env,cmd_env,expected_result",
    [
        [
            {"foo": "bar"},
            {"baz": "buz"},
            {"derp": "herp"},
            {"foo": "bar", "baz": "buz", "derp": "herp"},
        ],
        [{}, {"baz": "buz"}, {"derp": "herp"}, {"baz": "buz", "derp": "herp"}],
        [{"foo": "bar"}, {}, {"derp": "herp"}, {"foo": "bar", "derp": "herp"}],
        [{"foo": "bar"}, {"baz": "buz"}, {}, {"foo": "bar", "baz": "buz"}],
        [{"foo": "A"}, {"foo": "B"}, {"foo": "C"}, {"foo": "C"}],
        [{"foo": "A"}, {"foo": "B"}, {}, {"foo": "B"}],
        [{"foo": "A"}, {}, {"foo": "C"}, {"foo": "C"}],
        [{}, {"foo": "B"}, {"foo": "C"}, {"foo": "C"}],
        [{"foo": "A"}, {}, {}, {}],
        [{}, {"foo": "B"}, {}, {"foo": "B"}],
        [{}, {}, {"foo": "C"}, {"foo": "C"}],
    ],
)
def test_compile_environment(os_environ, global_env, cmd_env, expected_result):
    # Arrange
    # Act
    with patch.dict(main.os.environ, os_environ, clear=True):
        result = main.compile_environment(cmd_env, global_env)

    # Assert
    assert result == expected_result


def test_command_detail_prints_to_stdout(capfd):
    # Arrange
    config = {"commands": {"foo": {"cmd": ["derp", "herp"]}}}

    # Act
    main.command_detail("foo", config["commands"]["foo"])
    out, err = capfd.readouterr()

    # Assert
    assert out == textwrap.dedent(
        """
        foo:
          cmd:
          - derp
          - herp

    """
    )


def test_list_options_prints_output(capfd):
    # Arrange
    config = get_sample_config()

    # Act
    main.list_options(config)
    out, err = capfd.readouterr()

    # Assert
    assert (
        out
        == textwrap.dedent(
            """
        Available commands from config:
         - testcmd

    """
        ).lstrip()
    )
