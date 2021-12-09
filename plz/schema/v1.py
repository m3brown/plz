command_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
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
