from plz.runner import run_command

try:
    from mock import patch, ANY
except ImportError:
    from unittest.mock import patch, ANY


def test_run_command_returns_tuple():
    # Arrange

    # Act
    result = run_command('echo test')

    # Assert
    assert(type(result) == tuple)
    assert(len(result) == 2)


def test_run_command_returns_exit_code():
    # Arrange

    # Act
    result = run_command('bash -c "exit 99"')

    # Assert
    assert(result[0] == 99)


def test_run_command_returns_output():
    # Arrange
    stdout = '\n'.join(["1", "2", "3", "4"])

    # Act
    result = run_command('bash -c "for x in `seq 1 4`; do echo $x; done"')

    # Assert
    assert(result[1] == stdout.split("\n"))


def test_run_command_prints_to_stdout(capsys):
    # Arrange
    stdout = '\n'.join(["1", "2", "3", "4"]) + "\n"

    # Act
    run_command('bash -c "for x in `seq 1 4`; do echo $x; done"')
    out, err = capsys.readouterr()

    # Assert
    assert out == stdout


def test_run_command_does_not_print_to_stdout_when_disabled(capsys):
    # Arrange

    # Act
    run_command('bash -c "for x in `seq 1 4`; do echo $x; done"',
                std_output=False)
    out, err = capsys.readouterr()

    # Assert
    assert out == ""


def test_run_command_simple_glob(capsys):
    # Arrange
    stdout = '\n'.join([
        "plz/__init__.py",
    ]) + "\n"

    # Act
    run_command('ls plz/__*.py')
    out, err = capsys.readouterr()

    # Assert
    assert out == stdout
