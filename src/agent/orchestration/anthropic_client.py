"""
Anthropic client for the LangGraph graph
"""

import os
from dotenv import load_dotenv


from langchain_anthropic import ChatAnthropic

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001", temperature=0, timeout=None, max_retries=2
)
