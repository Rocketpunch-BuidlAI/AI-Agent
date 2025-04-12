import os
from typing import List

from langchain.chat_models import init_chat_model
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pydantic import BaseModel

from rag.output import EditResponseFormatter
from rag.store import create_vector_store
from rag.templates import enhance_prompt

# Load keys
openai_key = os.getenv("OPENAI_API_KEY")
llm = init_chat_model("gpt-4o")


def load_coverletter(
    coverletter: str,
    id: str,
    role: str,
    experience: str,
):
    documents = []

    documents.append(
        Document(
            page_content=coverletter,
            metadata={"source": id, "role": role, "experience": experience},
        )
    )

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


class RetrievedDocument(BaseModel):
    source_id: str
    content: str


def generate(
    docs: List[Document], 
    selfIntroduction: str, 
    motivation: str, 
    relevantExperience: str, 
    futureAspirations: str, 
    metadata: str, 
    prompt: str
):
    docs_content = [
        RetrievedDocument(source_id=doc.metadata.get("id", "unknown"), content=doc.page_content)
        for doc in docs
    ]

    docs_content_str = "\n\n".join(
        f"Source ID: {doc.source_id}\nContent: {doc.content}" for doc in docs_content
    )

    messages = enhance_prompt.invoke(
        {
            "user_resume_selfIntroduction": selfIntroduction,
            "user_resume_motivation": motivation,
            "user_resume_relevantExperience": relevantExperience,
            "user_resume_futureAspirations": futureAspirations,
            "user_metadata": metadata,
            "context": docs_content_str,
            "custom_prompt": prompt,
        }
    )

    response = llm.with_structured_output(EditResponseFormatter).invoke(messages)

    res = EditResponseFormatter.model_validate(response)

    return {
        "text": res.text,
        "sources": merge_contributions(res.used_sources),
    }


def merge_contributions(sources):
    merged = {}
    for source in sources:
        source_id = source.id
        contributions = source.contributions
        if source_id in merged:
            merged[source_id] += contributions
        else:
            merged[source_id] = contributions

    return [
        {"id": source_id, "contributions": contributions}
        for source_id, contributions in merged.items()
    ]


def generate_cover_letter(
    selfIntroduction: str, 
    motivation: str, 
    relevantExperience: str, 
    futureAspirations: str, 
    metadata: str, 
    prompt: str
):
    docs = retrieve()
    result = generate(docs=docs, 
        selfIntroduction=selfIntroduction, 
        motivation=motivation, 
        relevantExperience=relevantExperience, 
        futureAspirations=futureAspirations, 
        metadata=metadata, 
        prompt=prompt
    )

    return result
