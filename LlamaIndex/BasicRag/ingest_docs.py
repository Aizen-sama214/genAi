from config import Config
from pinecone import Pinecone, ServerlessSpec
import os

pc = Pinecone(api_key=Config().pine_cone_api_key)

dataset_name = "basic-rag"
if dataset_name not in pc.list_indexes().names():
    pc.create_index(
        dataset_name,
        dimension=1536,
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

pinecone_index = pc.Index(dataset_name)

from llama_index.vector_stores.pinecone import PineconeVectorStore

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

from pathlib import Path
from llama_index.readers.file import PyMuPDFReader

loader = PyMuPDFReader()
documents = loader.load(file_path="../../Knowledge/data/llama2.pdf")

from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext

api_key = Config().openai_api_key
os.environ["OPENAI_API_KEY"] = api_key
storage_context = StorageContext.from_defaults(vector_store=vector_store)
splitter = SentenceSplitter(chunk_size=1024)
index = VectorStoreIndex.from_documents(
    documents, transformations=[splitter], storage_context=storage_context
)

