import numpy as np
import re


def clean_words(text):
    """
    Convert text into simple lowercase words.
    """

    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    stop_words = {
        "what",
        "is",
        "the",
        "a",
        "an",
        "are",
        "was",
        "were",
        "when",
        "where",
        "who",
        "how",
        "why",
        "does",
        "do",
        "of",
        "in",
        "on",
        "for",
        "to",
        "and",
        "or",
        "with",
        "this",
        "that",
        "my",
        "your",
        "can",
        "be"
    }

    return [
        word
        for word in words
        if word not in stop_words
    ]


def find_relevant_chunks(
    question_embedding,
    question,
    chunks,
    chunk_embeddings,
    top_k=3
):
    """
    Find the most relevant document chunks.

    Uses:
    1. Semantic similarity
    2. Keyword matching
    3. Exact phrase matching
    """

    question_words = clean_words(question)

    similarities = []

    for i, chunk_embedding in enumerate(chunk_embeddings):

        chunk_words = clean_words(chunks[i])

        # -----------------------------------
        # 1. Semantic similarity
        # -----------------------------------

        question_norm = np.linalg.norm(question_embedding)
        chunk_norm = np.linalg.norm(chunk_embedding)

        if question_norm == 0 or chunk_norm == 0:
            semantic_similarity = 0
        else:
            semantic_similarity = np.dot(
                question_embedding,
                chunk_embedding
            ) / (
                question_norm * chunk_norm
            )

        # -----------------------------------
        # 2. Keyword matching
        # -----------------------------------

        matching_words = 0

        for word in question_words:

            if word in chunk_words:
                matching_words += 1

        if len(question_words) > 0:

            keyword_score = (
                matching_words / len(question_words)
            )

        else:

            keyword_score = 0

        # -----------------------------------
        # 3. Exact phrase matching
        # -----------------------------------

        question_clean = " ".join(question_words)
        chunk_clean = " ".join(chunk_words)

        phrase_score = 0

        if (
            len(question_words) >= 2
            and question_clean in chunk_clean
        ):
            phrase_score = 1

        # -----------------------------------
        # 4. Strong keyword boost
        # -----------------------------------

        if keyword_score == 1:
            keyword_boost = 1
        elif keyword_score > 0:
            keyword_boost = 0.5
        else:
            keyword_boost = 0

        # -----------------------------------
        # 5. Combined score
        # -----------------------------------

        final_score = (
            (semantic_similarity * 0.30)
            + (keyword_boost * 0.55)
            + (phrase_score * 0.15)
        )

        similarities.append(
            (final_score, chunks[i])
        )

    # Highest score first
    similarities.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # Return best chunks
    relevant_chunks = []

    for score, chunk in similarities[:top_k]:

        relevant_chunks.append(chunk)

    return relevant_chunks