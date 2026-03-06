from mfdballm.types_action import Action, ActionType


def parse(response):

    if response.tool_calls:

        return Action(
            ActionType.TOOL,
            {
                "calls": response.tool_calls
            }
        )

    return Action(
        ActionType.FINISH,
        {
            "answer": response.text
        }
    )


# backward compatibility for tests
def parse_provider_response(response):
    return parse(response)
