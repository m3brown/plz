import pytest
from jsonschema.exceptions import ValidationError

from plz.schema import validate_configuration_data


def get_sample_schema():
    return {
        "commands": [
            {
                "id": "test",
                "cmd": "poetry run python -m pytest",
            },
            {
                "id": "setup",
                "cmd": "poetry install",
            },
        ]
    }


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
    schema["commands"][0]["cmd"] = [
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
    schema["commands"][0].pop("id")

    # Act
    with pytest.raises(ValidationError) as error_info:
        validate_configuration_data(schema)

    # Assert
    assert error_info.value.message == "'id' is a required property"


@pytest.mark.parametrize(
    "id,expect_pass",
    [
        ["foo", True],
        ["foo1", True],
        ["1foo", True],
        ["foo_bar", True],
        ["foo-bar", True],
        ["foo bar", False],
        [" foo", False],
    ],
)
def test_validate_command_id(id, expect_pass):
    # Arrange
    schema = get_sample_schema()
    schema["commands"][0]["id"] = id

    # Act
    if expect_pass:
        validate_configuration_data(schema)
    else:
        with pytest.raises(ValidationError) as error_info:
            validate_configuration_data(schema)


def test_validate_command_without_cmd_fails():
    # Arrange
    schema = get_sample_schema()
    schema["commands"][0].pop("cmd")

    # Act
    with pytest.raises(ValidationError) as error_info:
        validate_configuration_data(schema)

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
    schema = get_sample_schema()
    if is_global:
        schema["global_env"] = {key: value}
    else:
        schema["commands"][0]["env"] = {key: value}

    # Act
    if expect_pass:
        validate_configuration_data(schema)
    else:
        with pytest.raises(ValidationError) as error_info:
            validate_configuration_data(schema)
