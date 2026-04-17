import json
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

class DisplayResults:
    def __init__(self,usecase,graph,user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        
    def display(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        
        if usecase == "Basic Chatbot":
            # Create proper message format
            initial_state = {'messages': [HumanMessage(content=user_message)]}
            
            # Display user message
            with st.chat_message("user"):
                st.write(user_message)
            
            # Stream the response
            for event in graph.stream(initial_state):
                for value in event.values():
                    if 'messages' in value:
                        # Display assistant response
                        with st.chat_message("assistant"):
                            st.write(value['messages'][-1].content)  # Get the last message
        
        elif usecase == "Chatbot With Web":
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)
            for message in res['messages']:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                elif isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.write(f"Tool Response: {message.content}")
                elif isinstance(message, AIMessage) and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
                        
        elif usecase == "AI News Summarizer":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news articles..."):
                result = graph.invoke({"messages":frequency})
                try:
                    news_path = f"./News/news_summary_{frequency}.txt"
                    with open(news_path, "r") as file:
                        summary_content = file.read()
                        st.markdown(summary_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"Summary file not found for {frequency} news. Please ensure the news fetching and summarization process completed successfully.")
                except Exception as e:
                    st.error(f"Error loading news summary: {e}")