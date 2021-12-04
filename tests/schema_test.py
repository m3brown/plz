from jsonschema.exceptions import ValidationError
from plz.schema import validate_configuration_data
import pytest


def get_sample_schema():
    return [
        {
            "id": "test",
            "cmd": "poetry run python -m pytest",
        },
        {
            "id": "setup",
            "cmd": "poetry install",
        },
    ]


def test_validate_happy_path_succeeds():
    # Arrange
    schema = get_sample_schema()

    # Act
    validate_configuration_data(schema)

    # Assert
    pass  # exception was not raised


def test_validate_command_array_succeeds():
    # Arrange
    schema = get_sample_schema()
    schema[0]["cmd"] = [
        "poetry install",
        "poetry run pre-commit install",
    ]

    # Act
    validate_configuration_data(schema)

    # Assert
    pass  # exception was not raised


def test_validate_command_without_id_fails():
    # Arrange
    schema = get_sample_schema()
    schema[0].pop("id")

    # Act
    with pytest.raises(ValidationError) as error_info:
        validate_configuration_data(schema)

    # Assert
    assert error_info.value.message == "'id' is a required property"


def test_validate_command_without_cmd_fails():
    # Arrange
    schema = get_sample_schema()
    schema[0].pop("cmd")

    # Act
    with pytest.raises(ValidationError) as error_info:
        validate_configuration_data(schema)

    # Assert
    assert error_info.value.message == "'cmd' is a required property"
