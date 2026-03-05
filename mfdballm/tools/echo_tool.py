echo_tool = {
    "name": "echo",
    "description": "Echo a message",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Text to echo"
            }
        },
        "required": ["text"]
    }
}
