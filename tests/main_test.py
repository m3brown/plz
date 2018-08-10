from plz.main import main
import pytest

try:
    from mock import patch, call
except ImportError:
    from unittest.mock import patch, call


def test_main_with_no_argument():
    # Arrange
    # Act
    # Assert
    with pytest.raises(SystemExit):
        main([])


@patch('plz.main.execute_from_config')
def test_main_with_single_argument(mock_execute):
    # Arrange
    # Act
    main(['testcmd'])

    # Assert
    mock_execute.assert_called_with('testcmd', [])


@patch('plz.main.execute_from_config')
def test_main_with_passthrough_argument(mock_execute):
    # Arrange
    # Act
    main(['testcmd', 'arg1'])

    # Assert
    mock_execute.assert_called_with('testcmd', ['arg1'])


@patch('plz.main.execute_from_config')
def test_main_with_several_passthrough_arguments(mock_execute):
    # Arrange
    # Act
    main(['testcmd', 'arg1', 'arg2', 'arg3'])

    # Assert
    mock_execute.assert_called_with('testcmd', ['arg1', 'arg2', 'arg3'])
