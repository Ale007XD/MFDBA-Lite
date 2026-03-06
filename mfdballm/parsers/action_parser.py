from mfdballm.types_action import Action, ActionType


def parse_provider_response(response):

    if getattr(response, "tool_calls", None):

        return Action(
            ActionType.TOOL,
            {"calls": response.tool_calls}
        )

    return Action(
        ActionType.FINISH,
        {"answer": response.text}
    )
