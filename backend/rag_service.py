from chunking import split_text_into_chunks
from embeddings import create_embeddings, create_question_embedding
from search import find_relevant_chunks


def create_document_index(document_text):

    chunks = split_text_into_chunks(
        document_text,
        chunk_size=1000,
        overlap=200
    )

    chunk_embeddings, vectorizer = create_embeddings(chunks)

    return {
        "chunks": chunks,
        "embeddings": chunk_embeddings,
        "vectorizer": vectorizer
    }


def retrieve_relevant_chunks(document_index, question):

    question_embedding = create_question_embedding(
        question,
        document_index["vectorizer"]
    )

    relevant_chunks = find_relevant_chunks(
        question_embedding,
        question,
        document_index["chunks"],
        document_index["embeddings"],
        top_k=3
    )

    return relevant_chunks