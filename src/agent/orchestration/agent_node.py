"""
Agent nodes for the LangGraph graph
"""

from langgraph.graph import MessagesState
from agent.orchestration.anthropic_client import model
from dance_mcp.client.langchain_mcp_client import client


# is this a good place to use async?
async def agent_node(state: MessagesState):
    """
    Agent node that uses the Anthropic model to generate a response
    """
    # type of response is class 'langchain_core.messages.ai.AIMessage'
    # which inherits from BaseMessage
    print("this agent node was called")
    tools = await client.get_tools()

    llm_model = model.bind_tools(tools)
    response = await llm_model.ainvoke(state["messages"])
    print("Agent response tool_calls:", response.tool_calls)
    print("Agent response has tool_calls?", bool(response.tool_calls))
    # value of messages is a list of messages, such as AIMessage, HumanMessage etc.
    return {"messages": [response]}
