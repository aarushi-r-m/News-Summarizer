from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class NewsSummarizerNode:
    def __init__(self, llm):
        from config import TAVILY_API_KEY
        self.tavily  = TavilyClient(api_key=TAVILY_API_KEY)
        self.llm = llm
        self.state = {}
    
    def fetch_news(self, state:dict) -> dict:
        frequency = state['messages'][0].content.lower()
        self.state['frequency']= frequency
        time_range_map = {"daily":"d", "weekly":"w", "monthly":"m", "yearly":"y"}
        days_map = {"daily":1, "weekly":7, "monthly":30, "yearly":366}
        
        response = self.tavily.search(
            query="Top news",
            topics="news",
            time_range=time_range_map.get(frequency),
            max_results=20,
            days=days_map[frequency],
            
        )
        
        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    
    
    def summarize_news(self, state:dict) -> dict:
        """This function takes the fetched news articles from the state, processes them using the LLM model to generate summaries,"
        """
        news_items = self.state['news_data']
        # Limit number of articles and content length to avoid token limit errors
        MAX_ARTICLES = 10  # You can adjust this
        MAX_CONTENT_LEN = 500  # You can adjust this (characters)
        limited_news = news_items[:MAX_ARTICLES]

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize news articles into markdown format. For each item include:
             - Date in *DD-MMM-YYYY* format in IST timezone
             - Concise sentences summary of the news
             -Sort news by date wise, latest first
             - Source URL as link
             User format:
             ###[Date]
             [Summary of the news](URL)"""),
            ("human","Articles:\n{articles}")
        ])

        articles_str = "\n\n".join(
            [
                f"Content:{item.get('content','')[:MAX_CONTENT_LEN]}\nDate:{item.get('date','N/A')}\nURL:{item.get('url','N/A')}"
                for item in limited_news
            ]
        )

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_result(self, state: dict) -> dict:
        """Save the news summary to a file"""
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./News/news_summary_{frequency}.txt"
        
        # Create News directory if it doesn't exist
        import os
        os.makedirs("./News", exist_ok=True)
        
        with open(filename, "w") as file:
            file.write(f"News Summary for {frequency.capitalize()}:\n\n")
            file.write(summary)
        self.state['filename'] = filename
        return self.state