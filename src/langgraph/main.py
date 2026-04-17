import streamlit as st
from src.langgraph.ui.streamlit.loadui import LoadStreamlitUI
from src.langgraph.LLMs.groqllm import GroqLLM
from src.langgraph.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph.graph.graph_builder import GraphBuilder
from src.langgraph.ui.streamlit.display_results import DisplayResults

def load_langgraph_app():
    """
    Loads and runs the Langgraph Agentic AI application using Streamlit.
    This function initializes the Streamlit UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    maintaining the state of the application."""
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: No use case selected.")
    
    
    user_message = st.text_input("Enter your message:")
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.selected_time_frame
    if user_message:
        try:
            obj_groq_llm = GroqLLM(user_control=user_input)
            model = obj_groq_llm.get_llm_model()
            
            if not model:
                st.error("Error: Failed to initialize the LLM model.")
                return
            
            usecase = user_input.get('selected_usecase')
            
            if not usecase:
                st.error("Error: No use case selected.")
                return
            graph_builder = GraphBuilder(model)
            try:
                if usecase == "AI News Summarizer":
                    tavily_api_key = user_input.get("TAVILY_API_KEY")
                    graph = graph_builder.setup_graph(usecase, tavily_api_key=tavily_api_key)
                else:
                    graph = graph_builder.setup_graph(usecase)
                DisplayResults(usecase, graph, user_message).display()
            except Exception as e:
                st.error(f"Error setting up the graph: {e}")
                return
               
        except Exception as e:
            st.error(f"Error initializing LLM model: {e}")
            return