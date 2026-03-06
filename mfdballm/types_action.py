from dataclasses import dataclass
from enum import Enum


class ActionType(str, Enum):

    TOOL = "TOOL"

    FINISH = "FINISH"


@dataclass
class Action:

    type: ActionType

    payload: dict
