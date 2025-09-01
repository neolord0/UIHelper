from langchain_core.prompts import PromptTemplate

from common import State
from util import parse_parameter, has_parameter


def label_creator(state: State):
    # print("\n\n======= Label Creator =======")

    prompt = PromptTemplate.from_template(
        """
        너는 UI 입력 도우미 팀의 글상자(라벨) 생성기이다.
        메시지(messages)를 분석하여 글상자(라벨) 생성에 필요한 파라메터 값들을 추출하고 parameters에 추가한다.
        필수적인 파라메터를 찾지 못하면 not_inputted_parameter_names 해당 파라메터 이름을 추가한다.
        필수적인 파라메터는 "텍스트(text)" 이나 "필드(field)" 이다.
        파라메터 값이 "텍스트(text)" 나 "필드(field)"를 선택할 때는 field_names을 참고한다.
        "텍스트(text)" 나 "필드(field)"를 찾으면 not_inputted_parameter_names의 내용을 모두 삭제한다.
        ---------------------------
        messages: {messages}
        ---------------------------
        field_names: {field_names}
        ---------------------------
        format_instructions: {format_instructions}
        """,
    )

    state = parse_parameter(prompt, state)

    if has_parameter("text", state["command"].parameters) | has_parameter("field", state["command"].parameters):
        state["not_inputted_parameter_names"] = []

    return state