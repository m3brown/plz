from plz.glob_tools import safe_glob

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


@patch('glob.glob')
def test_safe_glob_simple_glob(mock_glob):
    # Arrange
    mock_glob.return_value = ['glob_results.py']

    # Act
    result = safe_glob(['*.py'])

    # Assert
    assert result == ['glob_results.py']


@patch('glob.glob')
def test_safe_glob_multi_glob(mock_glob):
    # Arrange
    mock_glob.side_effect = [
        [],
        ['glob_results.py', 'more_results.py'],
        []
    ]
    # Act
    result = safe_glob(['test', '*.py', 'last'])

    # Assert
    assert result == ['test', 'glob_results.py', 'more_results.py', 'last']


@patch('glob.glob')
def test_safe_glob_non_matching_glob(mock_glob):
    # Arrange
    mock_glob.return_value = []
    # Act
    result = safe_glob(['*.py'])

    # Assert
    assert result == ['*.py']
