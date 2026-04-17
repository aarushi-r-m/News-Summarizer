from langgraph.graph import StateGraph, START, END
from src.langgraph.state.state import State
from src.langgraph.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import ToolNode,tools_condition
from src.langgraph.nodes.chatbot_with_web import ChatbotWithWebNode
from src.langgraph.nodes.news_summarizer_node import NewsSummarizerNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        
    def build_graph_for_chatbot(self):
        """
        Builds the graph based on the user message and the LLM model.
        This function takes the user message as input, processes it using the LLM model,
        and constructs a graph representation of the conversation or use case."""
        # Process user_message with self.llm to generate graph nodes and edges
        # For example, you might want to create nodes for each message and edges for the flow of conversation
        # This is a placeholder implementation and should be replaced with actual logic to build the graph
        
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
    
    def build_graph_for_chatbot_with_web(self):
        """
        Builds the graph for the "Chatbot With Web" use case.
        including nodes and edges that represent interactions with web data or APIs."""
        tools = get_tools()
        tool_node = create_tool_node(tools)
        llm = self.llm
        
        #Define the chatbot node
        obj_with_chatbot_node = ChatbotWithWebNode(llm)
        chatbot_node=obj_with_chatbot_node.create_chatbot(tools)
        
        #Add nodes to the graph
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        
        #Add edges to the graph
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def graph_for_news_summarizer(self):
        """
        Builds the graph for the "News Summarizer" use case.
        This function should construct a graph that represents the flow of fetching news articles,
        summarizing them using the LLM, and presenting the summaries to the user."""
        newsNode = NewsSummarizerNode(self.llm)
        
        #Added the nodes
        self.graph_builder.add_node("fetch_news", newsNode.fetch_news)
        self.graph_builder.add_node("summarize_news", newsNode.summarize_news)
        self.graph_builder.add_node("save_result", newsNode.save_result)
        
        #Added the edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)
        
        
    def setup_graph(self, usecase: str):
        """
        Sets up the graph based on the selected use case.
        This function determines which use case is selected by the user and calls the appropriate
        graph building function to construct the graph for that use case."""
        if usecase == "Basic Chatbot":
            self.build_graph_for_chatbot()
            return self.graph_builder.compile()
     
        if usecase == "Chatbot With Web":
            self.build_graph_for_chatbot_with_web()
            return self.graph_builder.compile()
        
        if usecase == "AI News Summarizer":
            self.graph_for_news_summarizer()
            return self.graph_builder.compile()