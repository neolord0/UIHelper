from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama

llm = ChatOllama(model="gpt-oss:20b")

from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field
from typing import Literal, Union

CommandType = Literal[
    "Nothing",
    "Set_Field",
    "Create_Table",
    "Create_Table_With_Row_Column_Count",
    "Create_Table_With_Fields",
    "Create_Label",
    "Create_SubReport",
    "Change_Property"
]

ParameterSort = Literal[
    "row_count", ### 행의 개수
    "column_count", ### 열의 개수
    "background_color", ### 배경색
    "font_color", ### 글자색
    "font_size", ### 글자 크기
    "font_family", ### 글꼴
    "text", ### 텍스트
    "field",  ### 필드
    "field_list" ###  필드 리스트
]

class Parameter(BaseModel):
    sort: ParameterSort = Field(..., description="sort of parameter")
    value: Union[str, int, float, list[str]] = Field(..., description="value of parameter")

class Command(BaseModel):
    type: CommandType = Field(..., description="type of command")
    parameters: list[Parameter] = Field(..., description="parameters of command")

class State(TypedDict):
    messages: list[AnyMessage | str]
    field_names: list[str]
    command: Command
    not_inputted_parameter_names: list[str]
    error: str | None
    output: str | None
