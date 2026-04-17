import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    """Groq LLM implementation using LangChain"""

    def __init__(self, user_control):
        self.user_control = user_control
    
    def get_llm_model(self):
        try:
            groq_api_key = self.user_control.get("GROQ_API_KEY")
            selected_groq_model = self.user_control.get("selected_model")
            
            if not groq_api_key and os.environ.get("GROQ_API_KEY", "") == '':
                st.error("Please Enter the Groq API Key to proceed.")
                return None
                
            # Use API key from user input if provided, otherwise from environment
            api_key = groq_api_key or os.environ.get("GROQ_API_KEY")
            
            llm = ChatGroq(api_key=api_key, model=selected_groq_model)
        
        except Exception as e:
            st.error(f"Error initializing Groq LLM: {e}")
            return None
        return llm