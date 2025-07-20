import os
from dotenv import load_dotenv

# Load environment variables from .env file in the root directory
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(root_dir, '.env')
load_dotenv(dotenv_path)

class Config:
    def __init__(self):
        self.pine_cone_api_key = os.getenv("PINECONE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

    def __repr__(self):
        return f"Config(pine_cone_api_key={self.pine_cone_api_key}, openai_api_key={self.openai_api_key }, tavily_api_key={self.tavily_api_key})"

