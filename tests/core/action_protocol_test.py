from mfdballm.types_action import Action, ActionType


def main():

    a = Action(ActionType.FINISH, {"answer": "ok"})

    assert a.type == ActionType.FINISH

    print("ACTION PROTOCOL TEST PASSED")


if __name__ == "__main__":
    main()
