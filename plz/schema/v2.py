single_word_regex = "^[A-Za-z0-9_-]+$"

env_variables = {
    "type": "object",
    "patternProperties": {single_word_regex: {"type": "string"}},
    "additionalProperties": False,
}

command_obj_schema = {
    "type": "object",
    "properties": {
        "cmd": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ]
        },
        "env": env_variables,
        "description": {"type": "string"},
    },
    "required": ["cmd"],
    "additionalProperties": False,
}

command_schema = {
    "anyOf": [
        command_obj_schema,
        {"type": "string"},
        {"type": "array", "items": {"type": "string"}},
    ]
}

schema = {
    "type": "object",
    "properties": {
        "commands": {
            "type": "object",
            "patternProperties": {single_word_regex: command_schema},
            "additionalProperties": False,
        },
        "global_env": env_variables,
        "shortcuts": env_variables,
    },
    "additionalProperties": False,
}
