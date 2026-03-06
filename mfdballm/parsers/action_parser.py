from mfdballm.types_action import Action, ActionType


def parse_provider_response(response):

    if response.tool_calls:

        calls = []

        for call in response.tool_calls:

            calls.append(
                {
                    "name": call.name,
                    "arguments": call.arguments,
                }
            )

        return Action(ActionType.TOOL, calls)

    if response.text:

        return Action(ActionType.FINISH, {"answer": response.text})

    return Action(ActionType.ERROR, {})
