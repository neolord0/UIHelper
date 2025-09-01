from langchain_core.prompts import PromptTemplate

from common import State
from util import parse_parameter

def property_changer(state: State):
    # print("\n\n======= Property Changer =======")

    prompt = PromptTemplate.from_template(
        """
        너는 UI 입력 도우미 팀의 속성 변경자 이다.
        메시지(messages)를 분석하여 변경할 속성에 대항하는 파라메터 이름과 값을 추출하여 parameters에 추가한다.
        ---------------------------
        messages: {messages}
        ---------------------------
        format_instructions: {format_instructions}
        """,
    )

    return parse_parameter(prompt, state)