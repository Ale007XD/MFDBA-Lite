from mfdballm.types_action import Action, ActionType

a = Action(ActionType.FINISH, {"answer": "ok"})

assert a.type == ActionType.FINISH

print("ACTION MODEL TEST PASSED")
