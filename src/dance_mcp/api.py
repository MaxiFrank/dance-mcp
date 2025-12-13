from fastapi import FastAPI
from agent.orchestration import dance_graph
import asyncio

app = FastAPI()


@app.get("/chats")
async def chats():
    result = await root()
    return result

async def root():
    """
    Main function to run the LangGraph graph
    """
    # Currently this does not add user message to state
    # there's no mechanism for adding any messages to state right now? Is that true?
    # or is this supposed to be in the agent node?
    # Explore streaming, like the projects I am familiar with.
    graph = dance_graph.set_up_graph()
    user_input = input("Enter your request: ")
    response = await graph.ainvoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )
    return response