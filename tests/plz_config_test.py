from plz.config import plz_config, load_config
from io import StringIO
import pytest
import sys

if sys.version_info.major > 2:
    from unittest.mock import patch
    builtins_module = 'builtins'
else:
    from mock import patch
    builtins_module = '__builtin__'


@patch('os.path.isfile')
@patch('plz.config.load_config')
def test_plz_config_detects_local_file(mock_load_config, mock_isfile):
    # Arrange
    mock_isfile.return_value = True

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with('.plz.yaml')


@patch('os.path.isfile')
@patch('plz.config.git_root')
@patch('plz.config.load_config')
def test_plz_config_falls_back_to_git_root_file(mock_load_config, mock_git_root, mock_isfile):
    # Arrange
    test_path = '/test/root/path'
    mock_git_root.return_value = test_path
    mock_isfile.return_value = False

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with('{}/.plz.yaml'.format(test_path))


@patch('os.path.isfile')
@patch('plz.config.git_root')
def test_plz_config_aborts_if_empty_git_root(mock_git_root, mock_isfile):
    # Arrange
    mock_git_root.return_value = ''
    mock_isfile.return_value = False

    # Act
    # Assert
    with pytest.raises(Exception):
        plz_config()


@patch('os.path.isfile')
@patch('plz.config.git_root')
def test_plz_config_aborts_if_null_root(mock_git_root, mock_isfile):
    # Arrange
    mock_git_root.return_value = None
    mock_isfile.return_value = False

    # Act
    # Assert
    with pytest.raises(Exception):
        plz_config()


@patch('os.path.isfile')
@patch('plz.config.git_root')
@patch('plz.config.load_config')
def test_plz_config_handles_extra_trailing_slash(mock_load_config, mock_git_root, mock_isfile):
    # Arrange
    test_path = '/test/root/path'
    mock_git_root.return_value = test_path + "/"
    mock_isfile.return_value = False

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with('{}/.plz.yaml'.format(test_path))


@patch('{}.open'.format(builtins_module))
def test_laod_config_loads_yaml_file(mock_open):
    # Arrange
    mock_open.return_value = StringIO(u"""- id: run
  name: runserver
  cmd: echo "./manage.py runserver"
""")
    expected_result = [{
        "id": "run",
        "name": "runserver",
        "cmd": 'echo "./manage.py runserver"',
    }]

    # Act
    result = load_config('path')

    # Assert
    assert(result == expected_result)
