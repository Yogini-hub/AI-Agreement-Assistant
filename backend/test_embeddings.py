from chunking import split_text_into_chunks
from embeddings import create_embeddings

text = """
The tenant must pay rent before the fifth day of every month.
The security deposit is fifty thousand rupees.
The tenant must provide sixty days notice before leaving.
The tenant is responsible for utility payments.
"""

chunks = split_text_into_chunks(
    text,
    chunk_size=100,
    overlap=20
)

embeddings = create_embeddings(chunks)

print("Number of chunks:", len(chunks))
print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))