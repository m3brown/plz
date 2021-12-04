from jsonschema import validate

command_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},  # todo: single_word_string
        "cmd": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
    },
    "required": ["id", "cmd"],
}

schema = {
    "type": "array",
    "items": command_schema,
}


def validate_configuration_data(parsed_data):
    validate(parsed_data, schema)
