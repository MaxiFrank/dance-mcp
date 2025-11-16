"""
Main graph for the LangGraph graph to orchestrate the dance and spotify tools
"""

from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import ToolMessage
from agent.orchestration.agent_node import agent_node
from dance_mcp.client.langchain_mcp_client import client


async def dance_tool_node(state: MessagesState):
    """
    Use langgraph mcp adapters to execute the dance tools
    """
    tools = await client.get_tools()
    message = state["messages"][-1]
    print("dance_tool_node called - message:", message)
    print("dance_tool_node - tool_calls:", message.tool_calls)
    # dance_tool_node - tool_calls: [{'name': 'search_by_difficulty',
    # 'args': {'difficulty': 'beginner'}, 'id': 'toolu_01BWRk6ZqadCS4JMoGw41iBW',
    # 'type': 'tool_call'},
    tool_messages = []
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_call_id = tool_call["id"]
            tool_name = tool_call["name"]
            tool = [t for t in tools if t.name == tool_name][0]
            result = await tool.ainvoke(input=tool_call["args"])
            tool_message = ToolMessage(
                tool_call_id=tool_call_id, tool_name=tool_name, content=result
            )
            tool_messages.append(tool_message)
            print("dance_tool_node - response:", result)
    return {"messages": tool_messages}


async def spotify_tool_node(state: MessagesState):
    """
    Use langgraph mcp adapters to execute the spotify tools
    """
    tools = await client.get_tools()
    message = state["messages"][-1]
    print("spotify_tool_node called - messages:", message)
    print("spotify_tool_node - tools calls:", message.tool_calls)
    tool_messages = []
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_call_id = tool_call["id"]
            tool_name = tool_call["name"]
            print("spotify_tool_node - tool_names", tool_name)
            # why the [0] element, what does tool_name look like?
            tool = [t for t in tools if t.name == tool_name][0]
            result = await tool.ainvoke(input=tool_call["args"])
            tool_message = ToolMessage(
                tool_call_id=tool_call_id, tool_name=tool_name, content=result
            )
            tool_messages.append(tool_message)
            print("spotify_tool_node - response:", result)
    return {"messages": tool_messages}


def placeholder_routing_post_agent(state: MessagesState):
    """
    determines the next node once the agent has completed its task
    if there's a tool call, route to the appropriate tool node,
    else route to END
    """
    # check if last message has tool cass
    # if last message has tool calls, route to tool node
    # if no tool calls, route to END
    message = state["messages"][-1]
    print("Routing - message tool_calls:", message.tool_calls)
    print("Routing - has tool_calls?", bool(message.tool_calls))
    if message.tool_calls:
        print("Routing to dance_tools")
        return "dance_tools"
    print("Routing to END")
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
