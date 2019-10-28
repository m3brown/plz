from plz.main import main, execute_from_config, list_options
import pytest
import sys

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


@patch('sys.exit')
@patch('plz.main.plz_config')
@patch('plz.main.list_options')
def test_main_with_no_argument_call_list_options(mock_list, mock_config, mock_exit):
    # Arrange
    mock_config.return_value = (
        [{'id': 'testcmd', 'cmd': 'derp'}],
        None
    )
    # Act
    main([])
    # Assert
    mock_list.assert_called_with(mock_config.return_value[0])


@patch.object(sys, 'argv', ['/root/path/plz', 'testcmd', 'arg1', 'arg2'])
@patch('plz.main.execute_from_config')
def test_main_with_sys_argv_parsing(mock_execute):
    # Arrange
    # Act
    main()

    # Assert
    mock_execute.assert_called_with('testcmd', ['arg1', 'arg2'])


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


@patch('sys.exit')
@patch('plz.main.gather_and_run_commands')
@patch('plz.main.plz_config')
def test_execute_from_config_with_valid_cmd(mock_plz_config, mock_gather, mock_exit):
    # Arrange
    args = ['args']
    mock_plz_config.return_value = (
        [{'id': 'testcmd', 'cmd': 'derp'}],
        None
    )

    # Act
    execute_from_config('testcmd', args)

    # Assert
    mock_gather.assert_called_with('derp', cwd=None, args=args)


@patch('sys.exit')
@patch('plz.main.gather_and_run_commands')
@patch('plz.main.plz_config')
def test_execute_from_config_with_valid_cmd_and_cwd(mock_plz_config, mock_gather, mock_exit):
    # Arrange
    args = ['args']
    cwd = '/root/path'
    mock_plz_config.return_value = (
        [{'id': 'testcmd', 'cmd': 'derp'}],
        cwd
    )

    # Act
    execute_from_config('testcmd', args)

    # Assert
    mock_gather.assert_called_with('derp', cwd=cwd, args=args)


@patch('sys.exit')
@patch('plz.main.plz_config')
def test_execute_from_config_with_invalid_cmd(mock_plz_config, mock_exit):
    # Arrange
    args = ['args']
    mock_plz_config.return_value = (
        [{'id': 'testcmd', 'cmd': 'derp'}],
        None
    )

    # Act
    execute_from_config('badcmd', args)

    # Assert
    mock_exit.assert_called_with(1)


@patch('sys.exit')
@patch('plz.main.plz_config')
def test_execute_from_config_with_valid_cmd_with_no_inner_cmd(mock_plz_config, mock_exit):
    # Arrange
    args = ['args']
    mock_plz_config.return_value = (
        [{'id': 'testcmd', 'noncmd': 'derp'}],
        None
    )

    # Act
    execute_from_config('testcmd', args)

    # Assert
    mock_exit.assert_called_with(1)


@patch('sys.exit')
@patch('plz.main.gather_and_run_commands')
@patch('plz.main.plz_config')
def test_execute_from_config_with_complex_cmd(mock_plz_config, mock_gather, mock_exit):
    # Arrange
    args = ['args']
    mock_plz_config.return_value = (
        [{'id': 'testcmd', 'cmd': ['derp', 'herp']}],
        None
    )

    # Act
    execute_from_config('testcmd', args)

    # Assert
    mock_gather.assert_called_with(['derp', 'herp'], cwd=None, args=args)


@patch('sys.exit')
@patch('plz.main.list_options')
@patch('plz.main.plz_config')
def test_execute_from_config_with_invalid_cmd_calls_list_options(mock_plz_config, mock_list, mock_exit):
    # Arrange
    args = ['args']
    mock_plz_config.return_value = (
        [{'id': 'testcmd', 'cmd': 'derp'}],
        None
    )

    # Act
    execute_from_config('badcmd', args)

    # Assert
    mock_list.assert_called_with(mock_plz_config.return_value[0])
