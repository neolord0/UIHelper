from langchain_core.prompts import PromptTemplate

from common import State, llm
from util import init_state, display


def communicator(state: State):
    # print("\n\n======= Communicator =======")

    if state["error"] is not None:
        display(f"error: {state['error']}", state)
        return init_state(state)

    prompt = PromptTemplate.from_template(
        """
        너는 UI 입력 도우미 팀의 커뮤니케이터이다.
        입력되지 않은 파라미터을 입력하도록 유도한다.
        not_inputted_parameter_names에 파라메털가 없으면, !Nothing!을 출력한다.
        입력을 유도하는 글은 간략하게 한줄로 작성한다.            
        ----------------------------
        not_inputted_parameter_names: {not_inputted_parameter_names}
        """
    )

    chain = prompt | llm

    output = chain.invoke({
        "not_inputted_parameter_names": state["not_inputted_parameter_names"]
    })

    if output.content.strip() != "!Nothing!":
        display(output.content, state)
        state["messages"].append(output)

    return state
