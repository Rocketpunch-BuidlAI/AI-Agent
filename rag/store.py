import os
import time

from pinecone import Pinecone, ServerlessSpec

pinecone_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(
    api_key=pinecone_key,
)

index_name = "cover-letter-enhancer"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)


def create_vector_store():
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import PineconeVectorStore

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    verctor_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
    )

    return verctor_store
