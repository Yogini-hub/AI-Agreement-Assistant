from chunking import split_text_into_chunks
from embeddings import create_embeddings
from search import find_relevant_chunks

text = """
The tenant must pay rent before the fifth day of every month.
The security deposit is fifty thousand rupees.
The tenant must provide sixty days notice before leaving.
The tenant is responsible for utility payments.
"""

# Split document into chunks
chunks = split_text_into_chunks(
    text,
    chunk_size=100,
    overlap=20
)

# Create embeddings for document chunks
chunk_embeddings = create_embeddings(chunks)

# Create embedding for the user's question
question = "What is the security deposit?"

question_embedding = create_embeddings([question])[0]

# Find relevant chunks
relevant_chunks = find_relevant_chunks(
    question_embedding,
    chunks,
    chunk_embeddings,
    top_k=2
)

print("Question:")
print(question)

print("\nRelevant chunks:")

for i, chunk in enumerate(relevant_chunks):
    print(f"\n--- Result {i + 1} ---")
    print(chunk)