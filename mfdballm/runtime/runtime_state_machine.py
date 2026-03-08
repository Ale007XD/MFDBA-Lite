from enum import Enum
from typing import Optional


class RuntimeState(str, Enum):
    """
    Возможные состояния runtime.
    """

    IDLE = "idle"
    RUNNING = "running"
    WAITING_FOR_TOOL = "waiting_for_tool"
    COMPLETED = "completed"
    ERROR = "error"


class RuntimeStateMachine:
    """
    Простая state machine для управления runtime.
    """

    def __init__(self) -> None:
        self.state: RuntimeState = RuntimeState.IDLE
        self.error: Optional[str] = None

    def start(self) -> None:
        if self.state != RuntimeState.IDLE:
            raise RuntimeError("Runtime can only start from IDLE")
        self.state = RuntimeState.RUNNING

    def wait_for_tool(self) -> None:
        if self.state != RuntimeState.RUNNING:
            raise RuntimeError("Can only wait for tool while RUNNING")
        self.state = RuntimeState.WAITING_FOR_TOOL

    def resume(self) -> None:
        if self.state != RuntimeState.WAITING_FOR_TOOL:
            raise RuntimeError("Can only resume from WAITING_FOR_TOOL")
        self.state = RuntimeState.RUNNING

    def complete(self) -> None:
        if self.state not in (RuntimeState.RUNNING, RuntimeState.WAITING_FOR_TOOL):
            raise RuntimeError("Runtime cannot complete from current state")
        self.state = RuntimeState.COMPLETED

    def fail(self, error: str) -> None:
        self.error = error
        self.state = RuntimeState.ERROR

    def is_finished(self) -> bool:
        return self.state in (RuntimeState.COMPLETED, RuntimeState.ERROR)
