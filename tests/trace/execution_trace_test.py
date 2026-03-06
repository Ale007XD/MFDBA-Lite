from mfdballm.execution.execution_trace import ExecutionTrace
from mfdballm.models.step_result import StepResult
from mfdballm.models.step_type import StepType


def main():

    trace = ExecutionTrace()

    step = StepResult(
        step_index=0,
        step_type=StepType.SYSTEM,
        input="hello",
        output="ok"
    )

    trace.add(step)

    assert len(trace.steps) == 1
    assert trace.last().step_type == StepType.SYSTEM

    print("TRACE TEST PASSED")


if __name__ == "__main__":

    main()
