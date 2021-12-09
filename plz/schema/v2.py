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
    },
    "additionalProperties": False,
}
