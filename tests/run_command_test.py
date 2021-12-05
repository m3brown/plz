import os
from unittest import skip

from plz.runner import run_command

try:
    pass
except ImportError:
    pass

starting_dir = os.getcwd()


def test_run_command_returns_int():
    # Arrange

    # Act
    result = run_command("echo test")

    # Assert
    assert type(result) == int


@skip("Error codes no longer supported")
def test_run_command_returns_exit_code():
    # Arrange

    # Act
    result = run_command('bash -c "exit 99"')

    # Assert
    assert result == 99


@skip("returning output not currently supported")
def test_run_command_returns_output():
    # Arrange
    stdout = "\n".join(["1", "2", "3", "4"])

    # Act
    result = run_command('bash -c "for x in `seq 1 4`; do echo $x; done"')

    # Assert
    assert result[1] == stdout.split("\n")


def test_run_command_prints_to_stdout(capfd):
    # Arrange
    stdout = "\n".join(["1", "2", "3", "4"]) + "\n"

    # Act
    run_command('bash -c "for x in `seq 1 4`; do echo $x; done"')
    out, err = capfd.readouterr()

    # Assert
    assert out == stdout


@skip("stdout parameter not currently supported")
def test_run_command_does_not_print_to_stdout_when_disabled(capfd):
    # Arrange

    # Act
    run_command('bash -c "for x in `seq 1 4`; do echo $x; done"', std_output=False)
    out, err = capfd.readouterr()

    # Assert
    assert out == ""


def test_run_command_accepts_env(capfd):
    # Arrange
    test_value = "this is a test"

    # Act
    run_command('bash -c "echo $FOO"', env={"FOO": test_value})
    out, err = capfd.readouterr()

    # Assert
    assert out == f"{test_value}\n"


def test_run_command_simple_glob(capfd):
    # Arrange
    stdout = "\n".join(["plz/__init__.py"]) + "\n"

    # Act
    run_command("ls plz/__*.py")
    out, err = capfd.readouterr()

    # Assert
    assert out == stdout


def test_run_command_glob_with_cwd(capfd):
    """
    Integration test

    Scenario: the plz.yaml file is "located" in the plz directory.

    In this case, the user will be running something like: `plz ls`
    """
    # Arrange
    os.chdir(starting_dir)
    stdout = "\n".join(["__init__.py"]) + "\n"
    cwd = os.path.join(os.getcwd(), "plz")

    # Act
    run_command("ls __*.py", cwd=cwd)
    out, err = capfd.readouterr()

    # Assert
    assert out == stdout


def test_run_command_glob_with_cwd_and_args(capfd):
    """
    Integration test

    Scenario: the plz.yaml file is "located" in the root of this repo, but
    the command is run from the child plz directory.

    In this case, the user will be running something like: `plz ls ../*.md`
    """

    # Arrange
    os.chdir(starting_dir)
    stdout = "\n".join(["README.md"]) + "\n"
    cwd = os.getcwd()
    os.chdir("plz")

    # Act
    run_command("ls", cwd=cwd, args=["../*.md"])
    out, err = capfd.readouterr()

    # Assert
    assert out == stdout
