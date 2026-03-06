from mfdballm.execution.execution_trace import ExecutionTrace
from mfdballm.execution.step_result import StepResult, StepType


def main():

    trace = ExecutionTrace()

    root = StepResult(
        step_type=StepType.SYSTEM,
        output="start",
    )

    trace.add(root)

    child = StepResult(
        step_type=StepType.MODEL,
        output="model",
        parent_step_id=root.step_id,
    )

    trace.add(child)

    assert trace.get(root.step_id) == root

    children = trace.children(root.step_id)

    assert len(children) == 1
    assert children[0] == child

    roots = trace.roots()

    assert len(roots) == 1
    assert roots[0] == root

    print("OK")


if __name__ == "__main__":
    main()
