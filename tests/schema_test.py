from unittest import skip

import pytest
from jsonschema.exceptions import ValidationError

from plz.schema import (
    DEPRECATED_SCHEMA_MESSAGE,
    DeprecatedSchemaException,
    validate_configuration_data,
)


def get_sample_config():
    return {
        "commands": {
            "test": {
                "cmd": "poetry run python -m pytest",
                "description": "run unit tests",
            },
            "setup": {
                "cmd": "poetry install",
            },
        }
    }


def test_validate_happy_path_succeeds():
    # Arrange
    config = get_sample_config()

    # Act
    validate_configuration_data(config)

    # Assert
    pass  # exception was not raised


def test_validate_command_array_succeeds():
    # Arrange
    config = get_sample_config()
    config["commands"]["test"]["cmd"] = [
        "poetry install",
        "poetry run pre-commit install",
    ]

    # Act
    validate_configuration_data(config)

    # Assert
    pass  # exception was not raised


@pytest.mark.parametrize(
    "id,expect_pass",
    [
        ["foo", True],
        ["foo1", True],
        ["1foo", True],
        ["1", True],
        [1, False],
        ["foo_bar", True],
        ["foo-bar", True],
        ["foo.bar", False],
        ["foo bar", False],
        [" foo", False],
    ],
)
def test_validate_command_id(id, expect_pass):
    # Arrange
    config = {"commands": {id: {"cmd": "test command"}}}

    # Act
    if expect_pass:
        validate_configuration_data(config)
    else:
        with pytest.raises(ValidationError) as error_info:
            validate_configuration_data(config)


def test_validate_command_without_cmd_fails():
    # Arrange
    config = get_sample_config()
    config["commands"]["test"].pop("cmd")

    # Act
    with pytest.raises(ValidationError) as error_info:
        validate_configuration_data(config)

    # Assert
    assert error_info.value.message == "'cmd' is a required property"


@pytest.mark.parametrize(
    "is_global",
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    "key,value,expect_pass",
    [
        ["foo", "bar", True],
        ["foo_bar", "bar", True],
        ["foo-bar", "bar", True],
        ["foo bar", "bar", False],
        ["foo", 'bash -c "echo Foo"', True],
        ["foo", 1, False],
        ["foo", "1", True],
        [1, "bar", False],
        ["1", "bar", True],
    ],
)
def test_validate_env(key, value, expect_pass, is_global):
    # Arrange
    config = get_sample_config()
    if is_global:
        config["global_env"] = {key: value}
    else:
        config["commands"]["test"]["env"] = {key: value}

    # Act
    if expect_pass:
        validate_configuration_data(config)
    else:
        with pytest.raises(ValidationError) as error_info:
            validate_configuration_data(config)


@skip("Temporarily disabled for soft deprecation")
def test_legacy_config_raises_DeprecatedSchemaException():
    # Arrange
    legacy_config = [
        {
            "id": "test",
            "cmd": "poetry run python -m pytest",
        },
        {
            "id": "setup",
            "cmd": "poetry install",
        },
    ]

    # Act
    # Assert
    with pytest.raises(DeprecatedSchemaException):
        validate_configuration_data(legacy_config)


@skip("Temporarily disabled for soft deprecation")
def test_legacy_config_prints_informational_message(capfd):
    # Arrange
    legacy_config = [
        {
            "id": "test",
            "cmd": "poetry run python -m pytest",
        },
        {
            "id": "setup",
            "cmd": "poetry install",
        },
    ]

    # Act
    try:
        validate_configuration_data(legacy_config)
    except Exception:
        pass
    out, err = capfd.readouterr()

    # Assert
    assert DEPRECATED_SCHEMA_MESSAGE in out
