from configparser import ConfigParser

class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            from pathlib import Path
            config_file = Path(__file__).resolve().parent / "streamlit" / "uiconfig.ini"

        self.config = ConfigParser()
        self.config.read(config_file)

    def get_page_title(self):
        return self.config['DEFAULT']['PAGE_TITLE']

    def get_llm_options(self):
        return self.config['DEFAULT']['LLM_OPTIONS'].split(',')

    def get_usecase_options(self):
        return self.config['DEFAULT']['USECASE_OPTIONS'].split(',')

    def get_groq_model_options(self):
        return self.config['DEFAULT']['GROQ_MODEL_OPTIONS'].split(',')