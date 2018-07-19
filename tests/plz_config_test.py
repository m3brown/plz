from plz.config import plz_config
from io import StringIO
import pytest
import sys

if sys.version_info.major > 2:
    from unittest.mock import patch
    builtins_module = 'builtins'
else:
    from mock import patch
    builtins_module = '__builtin__'


@patch('plz.config.git_root')
@patch('{}.open'.format(builtins_module))
def test_plz_config_loads_yaml_file(mock_open, mock_git_root):
    # Arrange
    test_path = '/test/root/path'
    mock_git_root.return_value = test_path
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
    result = plz_config()

    # Assert
    mock_open.assert_called_with('{}/.plz.yaml'.format(test_path))
    assert(result == expected_result)


@patch('plz.config.git_root')
def test_plz_config_aborts_if_empty_root(mock_git_root):
    # Arrange
    mock_git_root.return_value = ''

    # Act
    # Assert
    with pytest.raises(Exception):
        plz_config()


@patch('plz.config.git_root')
def test_plz_config_aborts_if_null_root(mock_git_root):
    # Arrange
    mock_git_root.return_value = None

    # Act
    # Assert
    with pytest.raises(Exception):
        plz_config()


@patch('plz.config.git_root')
@patch('{}.open'.format(builtins_module))
def test_plz_config_handles_extra_trailing_slash(mock_open, mock_git_root):
    # Arrange
    test_path = '/test/root/path'
    mock_git_root.return_value = test_path + "/"
    mock_open.return_value = StringIO(u'')

    # Act
    plz_config()

    # Assert
    mock_open.assert_called_with('{}/.plz.yaml'.format(test_path))
