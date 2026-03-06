from mfdballm.execution.execution_trace import ExecutionTrace
from mfdballm.execution.step_result import StepResult, StepType


def main():

    trace = ExecutionTrace()

    step1 = StepResult(
        step_type=StepType.SYSTEM,
        output="system start",
    )

    trace.add(step1)

    step2 = StepResult(
        step_type=StepType.MODEL,
        output="hello",
        parent_step_id=step1.step_id,
    )

    trace.add(step2)

    data = trace.to_dict()

    restored = ExecutionTrace.from_dict(data)

    assert len(restored.steps) == 2
    assert restored.steps[0].step_type == StepType.SYSTEM
    assert restored.steps[1].parent_step_id == restored.steps[0].step_id

    print("OK")


if __name__ == "__main__":
    main()
