import streamlit as st
import os

from src.langgraph.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_control={}
        
    def load_streamlit_ui(self):
        import os
        st.set_page_config(page_title= "🤖 "+ self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.timeFrame = ''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_control['llm_choice'] = st.selectbox("Select LLM", llm_options)

            if self.user_control['llm_choice'] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_control["selected_model"] = st.selectbox("Select Model", model_options)
                self.user_control["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("Groq API Key", value="", type="password")
                if not self.user_control["GROQ_API_KEY"]:
                    st.warning("⚠️Please enter your Groq API Key to proceed. You can create one from https://groq.com/ to use the Groq LLM.")

            self.user_control['selected_usecase'] = st.selectbox("Select Use Case", usecase_options)

            if self.user_control['selected_usecase'] == "Chatbot With Web" or self.user_control['selected_usecase'] == "AI News Summarizer":
                self.user_control["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Tavily API Key", value="", type="password")
                os.environ["TAVILY_API_KEY"] = self.user_control["TAVILY_API_KEY"]
                if not self.user_control["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY_API_KEY, you can create one from https://tavily.com/ to proceed with the selected use case.")

            if self.user_control['selected_usecase'] == "AI News Summarizer":
                st.subheader("📰 AI News Summarizer")
                with st.sidebar:
                    time_frame  = st.selectbox(
                        "Select Time Frame for News Articles",
                        ["Daily","Weekly", "Monthly"],
                        index=0
                    )
                if st.button("Fetch latest news", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.selected_time_frame = time_frame

            return self.user_control
        
        def save_result(self, state):
            frequency =self.state['frequency']
            summary = self.state['summary']
            filename = f"./News/news_summary_{frequency}.txt"
            with open(filename, "w") as file:
                file.write(f"News Summary for {frequency.capitalize()}:\n\n")
                file.write(summary)
            self.state['filename'] = filename
            return self.state
            