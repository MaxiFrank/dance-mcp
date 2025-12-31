"""
Agent nodes for the LangGraph graph
"""

from typing import List

from langgraph.graph import MessagesState
from agent.orchestration.anthropic_client import model
from dance_mcp.client.langchain_mcp_client import dance_client, spotify_client, scrape_data_client


# is this a good place to use async?
async def agent_node(state: MessagesState):
    """
    Agent node that uses the Anthropic model to generate a response
    """
    # type of response is class 'langchain_core.messages.ai.AIMessage'
    # which inherits from BaseMessage
    print("this agent node was called")
    dance_tools: List = await dance_client.get_tools()
    spotify_tools: List = await spotify_client.get_tools()
    data_scraping_tools = await scrape_data_client.get_tools()

    tools = dance_tools + spotify_tools + data_scraping_tools

    llm_model = model.bind_tools(tools)
    response = await llm_model.ainvoke(state["messages"])
    print("Agent response tool_calls:", response.tool_calls)
    print("Agent response has tool_calls?", bool(response.tool_calls))
    # value of messages is a list of messages, such as AIMessage, HumanMessage etc.
    return {"messages": [response]}

async def extract_urls_node(state: MessagesState):
    """
    Agent node that extracts URLs from scraped content using LLM
    Keeping this for now as I would want to keep this functionality for possible
    future usage
    """
    print("the extract_urls_node was called")
    scrape_data_tool: List = await scrape_data_client.get_tools()
    llm_model = model.bind_tools(scrape_data_tool)
    response = await llm_model.ainvoke(state["messages"])
    print("extract_urls_node response:", response)
    return {"messages": [response]}

async def dance_data_node(state: MessagesState):
    """
    Loops through URLS and calls scrape_url tool for each
    """
    import os, re

    print("dance_data_node is called")
    URL_DIR = "./data/urls"
    file_path = os.path.join(URL_DIR, "all_tiles_urls.txt")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return f"Error: File {file_path} not found. Run scrape_urls first."

    url_pattern = r'https://polepedia\.com/moves/[^\s\)]+'
    urls = re.findall(url_pattern, content)
    unique_urls = list(set(urls))
    print("unique urls", unique_urls[0])
    scrape_tools = await scrape_data_client.get_tools()
    scrape_url_tool = [t for t in scrape_tools if t.name == "scrape_url"][0]
    print("tools in scrape_url_tool", scrape_url_tool)
    
    # Loop through URLS and call tool for each
    for url in unique_urls:
        result = await scrape_url_tool.ainvoke({"url": url})
        print(result)
    
    print("dance_data_node finished - returning to END")
    return {"messages": [{"role": "assistant", "content": "Finished scraping all URLs"}]}