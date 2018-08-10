from plz.glob_tools import safe_glob, trim_prefix, absolute_glob, relative_glob

try:
    from mock import patch
except ImportError:
    from unittest.mock import patch


@patch('glob.glob')
def test_safe_glob_simple_glob(mock_glob):
    # Arrange
    mock_glob.return_value = ['glob_results.py']

    # Act
    match, result = safe_glob('*.py')

    # Assert
    assert match == True
    assert result == ['glob_results.py']


@patch('glob.glob')
def test_safe_glob_multi_glob(mock_glob):
    # Arrange
    mock_glob.return_value = ['glob_results.py', 'more_results.py']
    # Act
    match, result = safe_glob('*.py')

    # Assert
    assert match == True
    assert result == ['glob_results.py', 'more_results.py']


@patch('glob.glob')
def test_safe_glob_non_matching_glob(mock_glob):
    # Arrange
    mock_glob.return_value = []
    # Act
    match, result = safe_glob('*.py')

    # Assert
    assert match == False
    assert result == ['*.py']


@patch('glob.glob')
def test_absolute_glob(mock_glob):
    # Arrange
    mock_glob.return_value = [
        '/sample/root/glob_results.py', '/sample/root/more_results.py']

    # Act
    result = absolute_glob('*.py', cwd='/sample/root')

    # Assert
    assert list(result) == ['glob_results.py', 'more_results.py']


@patch('glob.glob')
def test_absolute_glob_with_no_match(mock_glob):
    # Arrange
    mock_glob.return_value = []

    # Act
    result = absolute_glob('*.py', cwd='/sample/root')

    # Assert
    assert result == ['*.py']


@patch('glob.glob')
def test_relative_glob_with_no_post_adjust_path(mock_glob):
    # Arrange
    mock_glob.return_value = ['../glob_results.py']

    # Act
    result = relative_glob('../*.py')

    # Assert
    assert result == ['../glob_results.py']


@patch('glob.glob')
def test_relative_glob_with_post_adjust_path(mock_glob):
    # Arrange
    mock_glob.return_value = ['glob_results.py']

    # Act
    result = relative_glob('*.py', post_adjust_path='test')

    # Assert
    assert list(result) == ['test/glob_results.py']


@patch('glob.glob')
def test_relative_glob_with_no_match_and_with_post_adjust_path(mock_glob):
    # Arrange
    mock_glob.return_value = []

    # Act
    result = relative_glob('*.py', post_adjust_path='test')

    # Assert
    assert result == ['*.py']
