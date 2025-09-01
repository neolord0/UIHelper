from fastapi import FastAPI, Request, Response
from starlette.middleware.sessions import SessionMiddleware

from util import init_state

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key="mysecretkey",
    session_cookie="session",
    max_age=None,
    path="/",
    same_site="lax",
    https_only=False)

from dotenv import load_dotenv
load_dotenv()

from graph_builder import graph_build
graph = graph_build()

from langchain_core.messages import HumanMessage

@app.get("/say/{user_input}")
async def say(user_input, request: Request, response: Response):
    state = request.session.get("state", init_state())

    state["messages"].append(HumanMessage(user_input))
    state = graph.invoke(state)

    response.headers["content-type"] = "text/plain; charset=utf-8"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    return state["output"]
