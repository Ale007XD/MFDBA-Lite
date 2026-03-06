from mfdballm.runtime.runtime_state_machine import RuntimeStateMachine


class RuntimeLoop:

    def __init__(self, engine, parser, tool_executor):
        self.engine = engine
        self.parser = parser
        self.tool_executor = tool_executor

    async def run(self, messages):

        state_machine = RuntimeStateMachine()
        current_messages = list(messages)

        last_response = None

        while not state_machine.is_finished():

            state_machine.transition_to_llm()

            response = await self.engine.execute(current_messages)
            last_response = response

            tool_calls = self.parser.parse(response)

            if not tool_calls:
                state_machine.finish()
                break

            state_machine.transition_to_tool()

            tool_results = await self.tool_executor.execute(tool_calls)

            for result in tool_results:
                current_messages.append(result)

        return last_response
