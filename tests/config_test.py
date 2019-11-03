from plz.config import plz_config, load_config, git_root, NoFileException, InvalidYamlException
from io import StringIO
import pytest
import sh
import sys

if sys.version_info.major > 2:
    from unittest.mock import patch, MagicMock, PropertyMock
    builtins_module = 'builtins'
else:
    from mock import patch, MagicMock, PropertyMock
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
    mock_isfile.side_effect = [False, True]

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with('{}/.plz.yaml'.format(test_path))


@patch('os.path.isfile')
@patch('plz.config.git_root')
@patch('plz.config.invalid_directory')
def test_plz_config_aborts_if_empty_git_root(mock_invalid_directory, mock_git_root, mock_isfile):
    # Arrange
    mock_git_root.return_value = ''
    mock_isfile.return_value = False

    # Act
    plz_config()

    # Assert
    mock_invalid_directory.assert_called_once_with()


@patch('os.path.isfile')
@patch('plz.config.load_config')
@patch('plz.config.invalid_yaml')
def test_plz_config_aborts_if_InvalidYamlException(mock_invalid_yaml, mock_load_config, mock_isfile):
    # Arrange
    mock_isfile.return_value = True
    mock_load_config.side_effect = InvalidYamlException("filename")

    # Act
    plz_config()

    # Assert
    mock_invalid_yaml.assert_called_once()


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
    mock_isfile.side_effect = [False, True]

    # Act
    plz_config()

    # Assert
    mock_load_config.assert_called_with('{}/.plz.yaml'.format(test_path))


@patch('{}.open'.format(builtins_module))
def test_load_config_loads_yaml_file(mock_open):
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


@patch('{}.open'.format(builtins_module))
def test_load_config_aborts_if_bad_yaml_file(mock_open):
    # Arrange
    mock_open.return_value = StringIO(u"""- id: run
  name: runserver
  cmd: echo "./manage.py runserver"
  foo
""")

    # Act
    # Assert
    with pytest.raises(InvalidYamlException):
        result = load_config('path')


@patch('sys.exit')
@patch('sh.Command')
def test_git_root_with_git_128_exception_raises_NoFileException(mock_sh, mock_exit):
    # Arrange
    mock_sh().side_effect = sh.ErrorReturnCode_128(b"", b"", b"")

    # Act
    # Assert
    with pytest.raises(NoFileException):
        git_root()


@patch('sh.Command')
def test_git_root_with_good_rc(mock_sh):
    # Arrange
    mock_sh_git = MagicMock()
    mock_sh_git.__repr__ = lambda x: '/sample/path'
    type(mock_sh_git).exit_code = PropertyMock(return_value=0)
    mock_sh().return_value = mock_sh_git

    # Act
    result = git_root()

    # Assert
    assert result == '/sample/path'
