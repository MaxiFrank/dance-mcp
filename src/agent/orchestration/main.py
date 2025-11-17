"""
Main module for the LangGraph graph
"""

import asyncio
from langchain_core.messages import HumanMessage
from agent.orchestration import dance_graph


def connect_to_graph():
    """
    Connect to the graph
    """
    graph = dance_graph.set_up_graph()
    return graph


async def main():
    """
    Main function to run the LangGraph graph
    """
    # Currently this does not add user message to state
    # there's no mechanism for adding any messages to state right now? Is that true?
    # or is this supposed to be in the agent node?
    # Explore streaming, like the projects I am familiar with.
    graph = connect_to_graph()
    messages = []
    user_input = input("Enter your request: ")
    while user_input != "q":
        user_message = HumanMessage(content=user_input)
        messages.append(user_message)
        response = await graph.ainvoke(
            {"messages": messages}
            # {"messages": [user_message]}
        )
        messages.extend(response["messages"])
        print("response in main.py is ", response)
        print("message in main.py is ", messages)
        user_input = input("Anything else: ")
    return response


if __name__ == "__main__":
    result = asyncio.run(main())
    for m in result["messages"]:
        m.pretty_print()
