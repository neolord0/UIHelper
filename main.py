from langchain_core.messages import HumanMessage

from graph_builder import graph_build
graph = graph_build()

from util import init_state
state = init_state()
while True:
    user_input = input("\nUser\t: ").strip()

    if user_input.lower() in ["exit", "quit", "q"]:
        print("\nBye!")
        break

    state["messages"].append(HumanMessage(user_input))
    state = graph.invoke(state)
