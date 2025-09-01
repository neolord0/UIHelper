from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from common import State, Parameter, llm

def table_creator_with_field_names(state: State):
    # print("\n\n======= Table Creator With Field Names =======")

    prompt = PromptTemplate.from_template(
        """
        너는 UI 입력 도우미 팀의 표 생성기(필드를 이용한)이다.
        메시지(messages)를 분석하여 표 생성에 필요한 파라메터 이름과 값을 추출하여 parameters에 추가한다.
        필드 이름(field_names)을 사용하여 필드 리스트(field_list) 파라메터를 생성한다.
        필드 이름(field_names)에 없는 필드 이름은 무시한다.
        ---------------------------
        messages: {messages}
        ---------------------------
        field_names: {field_names}
        ---------------------------
        format_instructions: {format_instructions}
        """,
    )

    class Result(BaseModel):
        parameters: list[Parameter]

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
        # print(f"Error during table creation: {e}")
        error = str(e)
        output = Result(
            parameters = [],
        )

    state["command"].parameters = output.parameters if output.parameters else []
    state["not_inputted_parameter_names"] = []
    state["error"] = error
    return state
