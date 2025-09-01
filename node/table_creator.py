from langchain_core.prompts import PromptTemplate

from common import State
from util import parse_parameter

def table_creator(state: State):
    # print("\n\n======= Table Creator =======")

    prompt = PromptTemplate.from_template(
        """
        너는 UI 입력 도우미 팀의 표 생성기이다.
        메시지(messages)를 분석하여 표 생성에 필요한 파라메터 이름과 값을 추출하여 parameters에 추가한다.
        필수적인 파라미터를 찾지 못하면 not_inputted_parameters에 해당 파라미터 이름을 추가한다.
        필수적인 파라메터는 "행의 개수", "열의 개수" 이다.
        ---------------------------
        messages: {messages}
        ---------------------------
        format_instructions: {format_instructions}
        """,
    )

    return parse_parameter(prompt, state)
