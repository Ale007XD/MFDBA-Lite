from mfdballm.runtime.runtime_state_machine import RuntimeStateMachine


def main():

    sm = RuntimeStateMachine()

    assert sm.state.value == "idle"

    sm.transition_to_llm()
    assert sm.state.value == "llm_call"

    sm.transition_to_tool()
    assert sm.state.value == "tool_exec"

    sm.transition_to_llm()
    assert sm.state.value == "llm_call"

    sm.finish()
    assert sm.is_finished()

    print("RUNTIME STATE MACHINE TEST PASSED")


if __name__ == "__main__":
    main()
