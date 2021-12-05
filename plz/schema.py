from jsonschema import exceptions, validate

single_word_regex = "^[A-Za-z0-9_-]+$"

env_variable_dict = {
    "type": "object",
    "patternProperties": {single_word_regex: {"type": "string"}},
    "additionalProperties": False,
}

command_schema = {
    "type": "object",
    "properties": {
        "cmd": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "env": env_variable_dict,
    },
    "required": ["cmd"],
    "additionalProperties": False,
}

schema = {
    "type": "object",
    "properties": {
        "commands": {
            "type": "object",
            "patternProperties": {single_word_regex: command_schema},
            "additionalProperties": False,
        },
        "global_env": env_variable_dict,
        "additionalProperties": False,
    },
}


def validate_configuration_data(parsed_data):
    try:
        validate(parsed_data, schema)
    except TypeError as e:
        integer_message = "expected string or bytes-like object"
        if str(e) == integer_message:
            raise exceptions.ValidationError(
                "Parsing exception: '{}'. Confirm all integer values in the plz.yaml config are wrapped in quotes.".format(
                    integer_message
                )
            )
        raise e
