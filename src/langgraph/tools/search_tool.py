from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """Return the list if toools to be used in the chatbot
    """
    tools=[TavilySearchResults(max_results=3)]
    return tools

def create_tool_node(tools):
    """Create tool nodes for the chatbot graph
    """
    return ToolNode(tools=tools)