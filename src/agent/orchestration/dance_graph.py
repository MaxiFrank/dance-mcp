"""
Main graph for the LangGraph graph to orchestrate the dance and spotify tools
"""

from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import ToolMessage
from agent.orchestration.agent_node import agent_node, dance_data_node
from dance_mcp.client.langchain_mcp_client import dance_client, spotify_client, fetch_mcp_client, scrape_data_client


async def tool_node(state: MessagesState):
    """
    Use langgraph mcp adapters to execute the tools
    """
    dance_tools = await dance_client.get_tools()
    spotify_tools = await spotify_client.get_tools()
    mcp_fetch_tool = await fetch_mcp_client.get_tools()
    data_scraping_tool = await scrape_data_client.get_tools()
    tools = dance_tools + spotify_tools + mcp_fetch_tool + data_scraping_tool

    message = state["messages"][-1]
    print("tool_node called - messages:", message)
    print("tool_node - tools calls:", message.tool_calls)
    tool_messages = []
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_call_id = tool_call["id"]
            tool_name = tool_call["name"]
            print("tool_node - tool_names", tool_name)
            # why the [0] element, what does tool_name look like?
            tool = [t for t in tools if t.name == tool_name][0]
            result = await tool.ainvoke(input=tool_call["args"])
            tool_message = ToolMessage(
                tool_call_id=tool_call_id, tool_name=tool_name, content=result
            )
            tool_messages.append(tool_message)
            print("tool_node - response:", result)
    return {"messages": tool_messages}

def url_exists(content: str) -> bool:
    """Check to see if url exists"""
    return "http" in content

async def routing_after_start(state: MessagesState):
    message = state["messages"][-1]
    # future use case
    # if url_exists(message.content):
    #     return "fetch_from_url"
    if "get online resource" in message.content.lower():
        return "dance_data"
    return "agent"

async def routing_post_agent(state: MessagesState):
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
        # What happens when there are multiple tool_calls?
        return "tools"
    print("Routing to END")
    return END


def set_up_graph():
    """
    Add nodes and edges to the graph and compile it
    """
    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.add_node("dance_data", dance_data_node)

    graph.add_conditional_edges(START, routing_after_start) # dance_data or agent
    graph.add_edge("dance_data", END)
    graph.add_conditional_edges("agent", routing_post_agent) # tools or end
    graph.add_edge("tools", "agent") # agent
    graph = graph.compile()
    return graph
