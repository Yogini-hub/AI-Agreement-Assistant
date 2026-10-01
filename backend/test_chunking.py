from chunking import split_text_into_chunks

text = """
This is a sample agreement document.
The tenant must pay rent before the fifth day of every month.
The security deposit is fifty thousand rupees.
The tenant must provide sixty days notice before leaving.
The tenant is responsible for utility payments.
"""

chunks = split_text_into_chunks(text, chunk_size=100, overlap=20)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\n--- Chunk", i + 1, "---")
    print(chunk)