import inspect
from langchain_community.tools.tavily_search import TavilySearchResults
print(inspect.signature(TavilySearchResults))
print(TavilySearchResults.__doc__)
