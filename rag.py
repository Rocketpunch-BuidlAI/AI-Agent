import os
import time

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import init_chat_model
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load keys
load_dotenv(dotenv_path=".env.local")
openai_key = os.getenv("OPENAI_API_KEY")
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


# 1. Embed and Upload Resumes to Pinecone
def load_resumes_to_pinecone(
    coverletter: str,
    metadata: dict,
):
    documents = []

    documents.append(
        Document(page_content=coverletter, metadata={"source": "user_coverletter", **metadata})
    )

    # Split and embed
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, add_start_index=True
    )
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    verctor_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
    )

    verctor_store.add_documents(docs)


# 2. RAG Query with Source Attribution
def enhance_resume(user_resume_text, target_company):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    verctor_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings,
    )
    retriever = verctor_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 5, "filter": {"company": target_company}}
    )

    llm = init_chat_model("gpt-4o")

    # Build RAG pipeline
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, return_source_documents=True, chain_type="stuff"
    )

    prompt = f"""
    You are a professional cover letter enhancer.

    Below is a candidate cover letter:
    ----------------------------
    {user_resume_text}

    Improve this coverletter to align with successful employees at {target_company}. 
    Use similar phrasing, highlight relevant skills, and make it ATS-friendly.

    Provide a rewritten version and cite relevant examples in brackets (e.g., [source]).
    """

    result = qa_chain(prompt)
    print("\n✅ Enhanced Coverletter:\n")
    print(result["result"])

    print("\n📚 Sources Used:")
    for doc in result["source_documents"]:
        print(f"- {doc.metadata['source']}")


# Run the pipeline
if __name__ == "__main__":
    # load_resumes_to_pinecone()
    sample_user_resume = """
    John Doe is a software engineer with 3 years of experience in backend development. 
    Skilled in Python and SQL. Worked on internal tools and small-scale APIs.
    """

    enhance_resume(sample_user_resume, target_company="Google")
