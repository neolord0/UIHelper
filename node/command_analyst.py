from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from common import State, llm, CommandType


def command_analyst(state: State):
    # print("\n\n======= Command Analyst =======")

    class Result(BaseModel):
        command_type: CommandType | None

    if state["command"].type == "Nothing":
        prompt = PromptTemplate.from_template(
            """
            너는 UI 입력 도우미 팀의 명령 분석가 다.
            메시지(messages)와 필드 이름(field_names)를 분석하여, 명령 타입(command_type)를 추출한다.
            이해할 수 없는 명령일 떄는 "Nothing"을 반환한다.
            표을 생성할 때, 필드 이름(field_names)에 나열된 필드를 찾으면 Create_Table_With_Fields를 반환한다.
            명령 타입는 다음과 같다:
            - Nothing: 이해할 수 없는 명령
            - Set_Field : 필드 설정
            - Create_Table: 표 생성
            - Create_Table_With_Row_Column_Count : 행과 열의 개수로 표 생성
            - Create_Table_With_Fields : 필드를 사용하여 표 생성
            - Create_Label: 글상자 생성
            - Change_Property : 속성 변경
    
            ----------------------------
            messages: {messages}
            ----------------------------
            field_names: {field_names}
            ---------------------------
            format_instructions: {format_instructions}
            """
        )

        parser = PydanticOutputParser(pydantic_object = Result)

        chain = prompt | llm | parser

        try:
            output = chain.invoke({
                "messages": state["messages"],
                "field_names": state["field_names"],
                "format_instructions": parser.get_format_instructions()
            })
        except Exception as e:
            # print(f"Error during table creation: {e}")
            output = Result(
                command_type = None
            )
    else:
        output = Result(
            command_type = state["command"].type
        )

    if output.command_type is None:
        state["command"].type = "Nothing"
        state["error"] = "명령을 이해할 수 없습니다."
    else:
        state["command"].type = output.command_type if output.command_type else None
        state["error"] = None

    return state


def command_analyst_router(state: State):
    return state["command"].type