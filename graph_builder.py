from langgraph.graph import StateGraph, START, END

from node.command_analyst import command_analyst, command_analyst_router
from node.communicator import communicator
from node.field_setter import field_setter
from node.label_creator import label_creator
from node.property_changer import property_changer
from node.report_command import report_command, is_complete_command
from node.table_creator import table_creator
from common import State
from node.table_creator_with_field_names import table_creator_with_field_names


def graph_build():
    graph_builder = StateGraph(State)

    graph_builder.add_node("command_analyst", command_analyst)
    graph_builder.add_node("table_creator", table_creator)
    graph_builder.add_node("label_creator", label_creator)
    graph_builder.add_node("property_changer", property_changer)  # Placeholder for future use
    graph_builder.add_node("table_creator_with_field_names", table_creator_with_field_names)
    graph_builder.add_node("field_setter", field_setter)
    graph_builder.add_node("report_command", report_command)
    graph_builder.add_node("communicator", communicator)

    graph_builder.add_edge(START, "command_analyst")
    graph_builder.add_conditional_edges(
        "command_analyst",
        command_analyst_router,
        {
            "Create_Table": "table_creator",
            "Create_Table_With_Row_Column_Count": "table_creator",
            "Create_Table_With_Fields" : "table_creator_with_field_names",
            "Change_Property": "property_changer",
            "Set_Field": "field_setter",
            "Nothing": "communicator"
        }
    )

    graph_builder.add_conditional_edges(
        "table_creator",
        is_complete_command,
        {
            True: "report_command",
            False: "communicator"
        }
    )
    graph_builder.add_conditional_edges(
        "label_creator",
        is_complete_command,
        {
            True: "report_command",
            False: "communicator"
        }
    )
    graph_builder.add_conditional_edges(
        "property_changer",
        is_complete_command,
        {
            True: "report_command",
            False: "communicator"
        }
    )
    graph_builder.add_conditional_edges(
        "table_creator_with_field_names",
        is_complete_command,
        {
            True: "report_command",
            False: "communicator"
        }
    )

    graph_builder.add_edge("field_setter", "communicator")
    graph_builder.add_edge("communicator", END)
    graph_builder.add_edge( "report_command", END)

    graph = graph_builder.compile()
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
    return graph