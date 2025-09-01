from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from common import State, llm
from util import init_state, display


def field_setter(state: State):
    # print("\n\n======= Field Setter =======")

    prompt = PromptTemplate.from_template(
        """
        너는 UI 입력 도우미 팀의 필드 설정하는 봇이다.
        메시지(messages)를 분석하여 필드 이름을 추출하여 반환하라.
        ---------------------------
        messages: {messages}
        ---------------------------
        format_instructions: {format_instructions}
        """,
    )

    class Result(BaseModel):
        field_names: list[str]

    parser = PydanticOutputParser(pydantic_object=Result)
    chain = prompt | llm | parser

    error = None
    try:
        output = chain.invoke({
            "messages": state["messages"],
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        # print(f"Error during table creation: {e}")

        error = str(e)
        output = Result(
            field_names = [],
        )

    state["field_names"] = output.field_names if output.field_names else []
    state["error"] = error

    if state["error"] is None and len(state["field_names"]) > 0:
        display(f"'''\n {len(state['field_names'])} fields were set\n'''", state)

    return init_state(state)
