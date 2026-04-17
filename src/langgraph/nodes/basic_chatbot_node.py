from src.langgraph.state.state import State
from langchain_core.messages import AIMessage

class BasicChatbotNode:
    def __init__(self, model):
        self.llm = model
        
    def process(self, state: State) -> dict:
        """
        This function processes the user message using the LLM model and generates a response.
        """
        # Get the last message (user's message)
        last_message = state['messages'][-1]
        
        # Invoke LLM with the message content
        response = self.llm.invoke(last_message.content)
        
        # Return the AI response as a new message
        return {"messages": [AIMessage(content=response.content)]}