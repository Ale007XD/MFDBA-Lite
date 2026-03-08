# Backward compatibility shim
# TODO: Remove shim after v0.40

from mfdballm.models.step_result import StepResult, StepType

__all__ = ["StepResult", "StepType"]
