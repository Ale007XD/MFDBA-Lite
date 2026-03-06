from mfdballm.execution.execution_trace import ExecutionTrace


def main():

    t = ExecutionTrace()

    t.add("step")

    assert len(t.steps) == 1

    print("TRACE TEST PASSED")


if __name__ == "__main__":

    main()
