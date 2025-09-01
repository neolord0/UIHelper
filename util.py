from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from common import State, llm, Parameter, ParameterSort, Command


def parse_parameter(prompt, state):
    class Result(BaseModel):
        parameters: list[Parameter]
        not_inputted_parameter_names: list[str] | None

    parser = PydanticOutputParser(pydantic_object=Result)
    chain = prompt | llm | parser
    error = None
    try:
        output = chain.invoke({
            "messages": state["messages"],
            "field_names": state["field_names"],
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        print(f"Error during table creation: {e}")
        error = str(e)
        output = Result(
            parameters = [],
            not_inputted_parameter_names =[]
        )

    state["command"].parameters = output.parameters if output.parameters else []
    state["not_inputted_parameter_names"] = output.not_inputted_parameter_names if output.not_inputted_parameter_names else []
    state["error"] = error
    return state


def has_parameter(sort : ParameterSort, parameters: list[Parameter]) -> bool:
    for parameter in parameters:
        if parameter.sort == sort:
            return True
    return False

def init_state(state:State = None) -> State:
    if state is None:
        state = State(
            messages = [
                SystemMessage(
                    """
                    너는 UI 입력 도우미 봇이다.
                    사용자의 입력을 받아서, 필요한 파라미터를 채우고, 명령을 완성하라.
                    파라미터 값으로 색상을 입력받을 경우, HEX 색상값으로 변환하여 설정하라.
                    사용자의 언어로 대화하라.
                    """
                )
            ],
            field_names = [],
            command = Command(
                type = "Nothing",
                parameters = [],
            ),
            not_inputted_parameter_names = [],
            error = None
        )
    else:
        state["messages"] = [
            SystemMessage(
                """
                너는 UI 입력 도우미 봇이다.
                사용자의 입력을 받아서, 필요한 파라미터를 채우고, 명령을 완성하라.
                파라미터 값으로 색상을 입력받을 경우, HEX 색상값으로 변환하여 설정하라.
                사용자의 언어로 대화하라.
                """
            )
        ]
        state["command"] = Command(
            type = "Nothing",
            parameters = []
        )
        state["not_inputted_parameter_names"] = []
        state["error"] = None
    return state

def command_to_dict(command: Command) -> dict:
    return ({
        "type": command.type,
        "parameters": [
            {
                "name": parameter.sort,
                "value": parameter.value,
            } for parameter in command.parameters
        ]
    }) if command else None

def display(message: str, state: State):
    state["output"] = message
    print(f"\nAI\t: {message}")
