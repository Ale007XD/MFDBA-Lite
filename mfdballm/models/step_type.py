from enum import Enum


class StepType(Enum):

    LLM_RESPONSE = "llm_response"

    TOOL_EXECUTION = "tool_execution"

    FINAL_ANSWER = "final_answer"

    SYSTEM = "system"
