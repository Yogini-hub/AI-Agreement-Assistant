from rag_service import retrieve_relevant_chunks


document_text = """
The tenant must pay rent before the fifth day of every month.
The security deposit is fifty thousand rupees.
The tenant must provide sixty days notice before leaving.
The tenant is responsible for utility payments.
The tenant cannot sublet the property without written permission.
"""

question = "What is the security deposit?"

relevant_chunks = retrieve_relevant_chunks(
    document_text,
    question
)

print("Question:")
print(question)

print("\nRetrieved chunks:")

for i, chunk in enumerate(relevant_chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)