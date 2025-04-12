import time

from langchain.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from rag import configs

# Initialize Pinecone
pc = Pinecone(api_key=configs.configs.pinecone)

index_name = "cv"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)


def create_vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    verctor_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
    )

    return verctor_store
