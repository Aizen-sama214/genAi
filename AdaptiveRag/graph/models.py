from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv


load_dotenv()

llm_model = ChatOpenAI(model="gpt-4o", temperature=0)  # I want to minimize hallucination - temperature = 0 makes the model output more deterministic

# Our Embedding Model - has to also be compatible with the LLM
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")