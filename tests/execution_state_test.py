from mfdballm.execution.execution_state import ExecutionState


def main():

    s = ExecutionState([{'role': 'user', 'content': 'hi'}])

    s.increment()

    assert s.iteration == 1

    print("EXECUTION STATE TEST PASSED")


if __name__ == "__main__":
    main()
