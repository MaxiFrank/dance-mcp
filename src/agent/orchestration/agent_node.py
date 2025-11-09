"""
Agent nodes for the LangGraph graph
"""

from langgraph.graph import MessagesState
from agent.orchestration.anthropic_client import model


def agent_node(state: MessagesState):
    """
    Agent node that uses the Anthropic model to generate a response
    """
    # type of response is class 'langchain_core.messages.ai.AIMessage'
    # which inherits from BaseMessage
    response = model.invoke(state["messages"])
    # value of messages is a list of messages, such as AIMessage, HumanMessage etc.
    return {"messages": [response]}
