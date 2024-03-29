import subprocess
import sys
import textwrap
from io import StringIO

import pytest

from plz.config import (
    DeprecatedSchemaException,
    InvalidYamlException,
    NoFileException,
    git_root,
    load_config,
    plz_config,
)
from plz.schema import validate_configuration_data

if sys.version_info.major > 2:
    from unittest.mock import patch

    builtins_module = "builtins"
else:
    from mock import patch

    builtins_module = "__builtin__"


@patch("os.path.isfile")
@patch("plz.config.load_config")
def test_plz_config_detects_local_file(mock_load_config, mock_isfile):
    # Arrange
    mock_isfile.return_value = True

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with("plz.yaml")


@patch("os.path.isfile")
@patch("plz.config.git_root")
@patch("plz.config.load_config")
def test_plz_config_falls_back_to_git_root_file(
    mock_load_config, mock_git_root, mock_isfile
):
    # Arrange
    test_path = "/test/root/path"
    mock_git_root.return_value = test_path
    mock_isfile.side_effect = [False, True]

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with("{}/plz.yaml".format(test_path))


@patch("os.path.isfile")
@patch("plz.config.git_root")
@patch("plz.config.load_config")
def test_plz_config_falls_back_to_legacy_filename(
    mock_load_config, mock_git_root, mock_isfile
):
    # Arrange
    mock_isfile.side_effect = [False, False, True]
    mock_git_root.return_value = "git"

    # Act
    plz_config()

    # Assert
    assert mock_isfile.call_count == 3
    mock_load_config.assert_called_with(".plz.yaml")


@patch("os.path.isfile")
@patch("plz.config.git_root")
@patch("plz.config.invalid_directory")
def test_plz_config_aborts_if_empty_git_root(
    mock_invalid_directory, mock_git_root, mock_isfile
):
    # Arrange
    mock_git_root.return_value = ""
    mock_isfile.return_value = False

    # Act
    plz_config()

    # Assert
    mock_invalid_directory.assert_called_once_with()


@patch("os.path.isfile")
@patch("plz.config.load_config")
@patch("plz.config.invalid_yaml")
def test_plz_config_aborts_if_InvalidYamlException(
    mock_invalid_yaml, mock_load_config, mock_isfile
):
    # Arrange
    mock_isfile.return_value = True
    mock_load_config.side_effect = InvalidYamlException("filename")

    # Act
    plz_config()

    # Assert
    mock_invalid_yaml.assert_called_once_with("filename")


@patch("os.path.isfile")
@patch("plz.config.git_root")
def test_plz_config_aborts_if_null_root(mock_git_root, mock_isfile):
    # Arrange
    mock_git_root.return_value = None
    mock_isfile.return_value = False

    # Act
    # Assert
    with pytest.raises(Exception):
        plz_config()


@patch("os.path.isfile")
@patch("plz.config.git_root")
@patch("plz.config.load_config")
def test_plz_config_handles_extra_trailing_slash(
    mock_load_config, mock_git_root, mock_isfile
):
    # Arrange
    test_path = "/test/root/path"
    mock_git_root.return_value = test_path + "/"
    mock_isfile.side_effect = [False, True]

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with("{}/plz.yaml".format(test_path))


@patch("{}.open".format(builtins_module))
def test_load_config_loads_yaml_file(mock_open):
    # Arrange
    mock_open.return_value = StringIO(
        textwrap.dedent(
            """
            commands:
              run:
                cmd: echo "./manage.py runserver"
            """
        )
    )
    expected_result = {"commands": {"run": {"cmd": 'echo "./manage.py runserver"'}}}

    # Act
    result = load_config("path")

    # Assert
    assert result == expected_result


@patch("{}.open".format(builtins_module))
def test_load_config_aborts_if_bad_yaml_file(mock_open):
    # Arrange
    mock_open.return_value = StringIO(
        textwrap.dedent(
            """
            commands:
              run:
                cmd: echo "./manage.py runserver"
                foo
            """
        )
    )

    # Act
    # Assert
    with pytest.raises(InvalidYamlException):
        load_config("path")


@patch("{}.open".format(builtins_module))
def test_load_config_aborts_if_file_does_not_match_schema(mock_open):
    # Arrange
    mock_open.return_value = StringIO(
        textwrap.dedent(
            """
            commands:
              run:
                cmd: echo "./manage.py runserver"
                foo: bar
            """
        )
    )

    # Act
    # Assert
    with pytest.raises(InvalidYamlException):
        load_config("path")


@patch("sys.exit")
@patch("subprocess.check_output")
def test_git_root_with_git_128_exception_raises_NoFileException(
    mock_check_output, mock_exit
):
    # Arrange
    mock_check_output.side_effect = subprocess.CalledProcessError(
        returncode=128, cmd="cmd"
    )

    # Act
    # Assert
    with pytest.raises(NoFileException):
        git_root()


@patch("subprocess.check_output")
def test_git_root_with_good_rc(mock_check_output):
    # Arrange
    mock_check_output.return_value = "/sample/path"

    # Act
    result = git_root()

    # Assert
    assert result == "/sample/path"


@pytest.mark.parametrize(
    "exception",
    [
        InvalidYamlException("foo"),
        NoFileException,
        DeprecatedSchemaException,
    ],
)
@patch("plz.config.find_file")
@patch("sys.exit")
def test_plz_config_exception_calls_sys_exit_1(mock_exit, mock_find_file, exception):
    # Arrange
    mock_find_file.side_effect = exception

    # Act
    plz_config()

    # Assert
    mock_exit.assert_called_once_with(1)


@patch("{}.open".format(builtins_module))
def test_load_config_with_legacy_formatprints_deprecation_message(mock_open, capfd):
    # Arrange
    mock_open.return_value = StringIO(
        textwrap.dedent(
            """
            - id: run
              cmd: echo "./manage.py runserver"
            - id: test
              cmd:
              - "poetry run python -m pytest"
            """
        )
    )

    # Act
    load_config("filename")
    out, err = capfd.readouterr()

    # Assert
    assert "DEPRECATION WARNING: Your plz.yaml file is using a deprecated format" in out


@patch("{}.open".format(builtins_module))
def test_load_config_converts_legacy_config_to_valid_config(mock_open):
    # Arrange
    mock_open.return_value = StringIO(
        textwrap.dedent(
            """
            - id: run
              cmd: echo "./manage.py runserver"
            - id: test
              cmd:
              - "poetry run python -m pytest"
            """
        )
    )

    # Act
    result = load_config("filename")

    # Assert
    assert type(result) == dict
    # Confirm validate_configuration_data does not throw an exception
    assert validate_configuration_data(result) == None
