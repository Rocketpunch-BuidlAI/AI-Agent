import os
from typing import List

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from rag.output import EditResponseFormatter
from rag.store import create_vector_store
from rag.templates import enhance_prompt

# Load keys

openai_key = os.getenv("OPENAI_API_KEY")
llm = init_chat_model("gpt-4o")


# 1. Embed and Upload Resumes to Pinecone
def load_coverletter(
    coverletter: str,
    metadata: dict,
):
    documents = []

    documents.append(
        Document(page_content=coverletter, metadata={"source": metadata.get("id"), **metadata})
    )

    # Split and embed
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, add_start_index=True
    )
    docs = text_splitter.split_documents(documents)

    vector_store = create_vector_store()
    vector_store.add_documents(docs)


def retrieve():
    vector_store = create_vector_store()

    retrieved_docs = vector_store.similarity_search(
        "Find coverletters from successful employees which are similar to the user coverletter",
        k=5,
    )

    return retrieved_docs


def generate(docs: List[Document], query: str):
    docs_content = "\n\n".join(
        f"Source ID: {doc.metadata.get('id', 'unknown')}\nContent: {doc.page_content}"
        for doc in docs
    )

    print("Retrieved documents:", docs_content)

    messages = enhance_prompt.invoke(
        {
            "user_resume_text": query,
            "context": docs_content,
        }
    )

    response = llm.with_structured_output(EditResponseFormatter).invoke(messages)

    print("Response from LLM:", response)
    return response


# 2. RAG Query with Source Attribution
def enhance_resume(user_resume_text):
    query = """
        
        My name is John Doe, and I am a software engineer with a passion for developing innovative solutions. I have a strong background in computer science and have worked on various projects that showcase my skills in programming, problem-solving, and teamwork. I am excited about the opportunity to contribute to your organization and help drive success through technology.
        I am particularly interested in the software engineering role at your company because of its commitment to innovation and excellence. I believe that my skills and experiences align well with the requirements of the position, and I am eager to bring my expertise to your team.
        I have a strong foundation in software development, having worked on several projects that involved designing and implementing software solutions. I am proficient in multiple programming languages, including Python, Java, and C++. I have also gained experience in working with databases and cloud technologies, which I believe will be valuable in this role.
        I am a quick learner and am always looking for opportunities to expand my knowledge and skills. I am particularly interested in learning more about cloud computing and machine learning, as I believe these areas will play a significant role in the future of software development.
        I am excited about the possibility of joining your team and contributing to the development of cutting-edge software solutions. I am confident that my skills, experiences, and passion for technology make me a strong candidate for this role.
        
        """

    docs = retrieve()
    result = generate(docs=docs, query=query)

    return result
