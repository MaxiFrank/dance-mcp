"""
Main module for the LangGraph graph
"""

from agent.orchestration import dance_graph

if __name__ == "__main__":
    graph = dance_graph.set_up_graph()
    user_input = input("Enter your request: ")
    response = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
    for m in response["messages"]:
        m.pretty_print()
