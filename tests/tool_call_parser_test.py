from mfdballm.tool_call_parser import parse_tool_calls
from mfdballm.types import ProviderResponse


def test_parser():

    response = ProviderResponse(
        text=None,
        tool_calls=[
            {
                "name": "echo",
                "arguments": {"text": "hello"}
            }
        ]
    )

    calls = parse_tool_calls(response)

    assert len(calls) == 1
    assert calls[0].name == "echo"
    assert calls[0].arguments["text"] == "hello"


if __name__ == "__main__":
    test_parser()
    print("tool_call_parser_test passed")
