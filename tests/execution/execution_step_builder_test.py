from mfdballm.execution.execution_step_builder import ExecutionStepBuilder
from mfdballm.models.step_type import StepType


def main():

    builder = ExecutionStepBuilder()

    step1 = builder.system("start")

    step2 = builder.llm_response(
        input="hello",
        output="hi"
    )

    step3 = builder.final_answer(
        output="done"
    )

    assert step1.step_index == 0
    assert step2.step_index == 1
    assert step3.step_index == 2

    assert step1.step_type == StepType.SYSTEM
    assert step2.step_type == StepType.LLM_RESPONSE
    assert step3.step_type == StepType.FINAL_ANSWER

    print("STEP BUILDER TEST PASSED")


if __name__ == "__main__":
    main()
