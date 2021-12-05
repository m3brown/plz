import re

from jsonschema import FormatChecker, exceptions, validate

single_word_regex = "^[A-Za-z0-9_-]+$"

env_variable_dict = {
    "type": "object",
    "patternProperties": {single_word_regex: {"type": "string"}},
    "additionalProperties": False,
}

plz_format_checker = FormatChecker()


@plz_format_checker.checks("single_word", TypeError)
def is_single_word(instance):
    return type(instance) == str and re.match(single_word_regex, instance)


command_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "format": "single_word"},  # todo: single_word_string
        "cmd": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "env": env_variable_dict,
    },
    "required": ["id", "cmd"],
}

schema = {
    "type": "object",
    "properties": {
        "commands": {
            "type": "array",
            "items": command_schema,
        },
        "global_env": env_variable_dict,
    },
}


def validate_configuration_data(parsed_data):
    try:
        validate(parsed_data, schema, format_checker=plz_format_checker)
    except TypeError as e:
        integer_message = "expected string or bytes-like object"
        if str(e) == integer_message:
            raise exceptions.ValidationError(
                f"Parsing exception: '{integer_message}'. Confirm all integer values in the .plz.yaml config are wrapped in quotes."
            )
        raise e
