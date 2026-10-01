from rag_service import retrieve_relevant_chunks
from gemini_service import answer_with_rag


document_text = """
The tenant must pay rent before the fifth day of every month.
The security deposit is fifty thousand rupees.
The tenant must provide sixty days notice before leaving.
The tenant is responsible for utility payments.
The tenant cannot sublet the property without written permission.
"""

question = "What is the security deposit?"

# Retrieve relevant chunks
relevant_chunks = retrieve_relevant_chunks(
    document_text,
    question
)

# Ask Gemini using only those chunks
answer = answer_with_rag(
    question,
    relevant_chunks
)

print("Question:")
print(question)

print("\nAnswer:")
print(answer)