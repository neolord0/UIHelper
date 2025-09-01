from common import State
from util import command_to_dict, init_state, display


def is_complete_command(state: State) -> bool:
    return (state["command"].type != "Nothing"
            and len(state["not_inputted_parameter_names"]) == 0
            and state["error"] is None)

def report_command(state: State):
    display("\n'''\n" + str(command_to_dict(state["command"])) + "\n'''", state)

    return init_state(state)