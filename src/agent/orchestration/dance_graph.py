"""
Main graph for the LangGraph graph to orchestrate the dance and spotify tools
"""

from langgraph.graph import StateGraph, MessagesState, START, END
from agent.orchestration.agent_node import agent_node


def dance_tool_node():
    """
    Eventually use langgraph mcp adapters to execute the tool
    """
    return {"messages": [{"role": "tool", "content": "dance tool executed"}]}


def spotify_tool_node():
    """
    Eventually use langgraph mcp adapters to execute the tool
    """
    return {"messages": [{"role": "tool", "content": "spotify tool executed"}]}


def placeholder_routing_post_agent():
    """
    determines the next node once the agent has completed its task
    """
    # check if last message has tool cass
    # if last message has tool calls, route to tool node
    # if no tool calls, route to END
    return END


def set_up_graph():
    """
    Add nodes and edges to the graph and compile it
    """
    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("dance_tools", dance_tool_node)
    graph.add_node("spotify_tools", spotify_tool_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", placeholder_routing_post_agent)
    graph.add_edge("dance_tools", "agent")
    graph.add_edge("spotify_tools", "agent")
    graph = graph.compile()
    return graph
