import os
import json
import time

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def is_rate_limit_error(error):
    error_text = str(error)

    return (
        "429" in error_text
        or "RateLimitError" in error_text
        or "rate limit" in error_text.lower()
        or "quota" in error_text.lower()
    )


def is_connection_error(error):
    error_text = str(error)

    connection_errors = [
        "APIConnectionError",
        "UNEXPECTED_EOF_WHILE_READING",
        "ConnectError",
        "SSL",
        "ConnectionError",
        "connection",
        "timeout",
        "timed out"
    ]

    return any(
        message.lower() in error_text.lower()
        for message in connection_errors
    )


def analyze_document(text):

    prompt = f"""
You are an assistant that helps users understand agreements and documents.

Analyze the document and return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "Simple summary of the document",
    "important_terms": [
        "Important term 1",
        "Important term 2"
    ],
    "attention_clauses": [
        "Clause the user should pay attention to"
    ],
    "financial_details": [
        "Rent, deposit, fee, penalty, or other financial detail"
    ],
    "important_dates": [
        "Important date and its meaning"
    ],
    "obligations": [
        "Important obligation of the user or other party"
    ]
}}

Rules:
- Use simple language.
- Only include information actually present in the document.
- Do not invent missing information.
- If a category has no information, return an empty list [].
- Do not provide legal advice.
- Return ONLY JSON.
- Do not use markdown or ```.

Document:
{text}
"""

    for attempt in range(2):

        try:

            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            result = interaction.output_text

            return json.loads(result)

        except Exception as error:

            print("Gemini analysis error:", error)

            if is_rate_limit_error(error):

                return {
                    "summary": "Gemini API limit has been reached. Please try again later.",
                    "important_terms": [],
                    "attention_clauses": [],
                    "financial_details": [],
                    "important_dates": [],
                    "obligations": []
                }

            if is_connection_error(error):

                if attempt == 0:
                    time.sleep(3)
                    continue

                return {
                    "summary": "Could not connect to the Gemini API. Please try again later.",
                    "important_terms": [],
                    "attention_clauses": [],
                    "financial_details": [],
                    "important_dates": [],
                    "obligations": []
                }

            if attempt == 1:

                return {
                    "summary": "The document could not be analyzed because of a Gemini API error.",
                    "important_terms": [],
                    "attention_clauses": [],
                    "financial_details": [],
                    "important_dates": [],
                    "obligations": []
                }

            time.sleep(3)


def ask_question(document_text, question):

    prompt = f"""
You are an assistant that helps users understand agreements and documents.

Answer the user's question using ONLY the information present in the document.

Rules:
- Use simple language.
- Give a short and direct answer.
- Maximum 3 short sentences.
- Start with the exact answer if possible.
- Do not repeat unnecessary parts of the document.
- Do not copy large portions of the document.
- Do not invent information.
- If the answer is not present in the document, say:
  "This information is not mentioned in the document."
- Do not provide legal advice.

Document:
{document_text}

User question:
{question}

Answer:
"""

    for attempt in range(2):

        try:

            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            return interaction.output_text

        except Exception as error:

            print("Gemini question error:", error)

            if is_rate_limit_error(error):

                return "Gemini API limit has been reached. Please try again later."

            if is_connection_error(error):

                if attempt == 0:
                    time.sleep(3)
                    continue

                return "Could not connect to the Gemini API. Please try again later."

            if attempt == 1:

                return "The Gemini API could not process the question right now."

            time.sleep(3)


def answer_with_rag(question, relevant_chunks):

    # Send the FULL retrieved chunks to Gemini.
    # We only shorten sources later in the frontend if needed.
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an assistant that helps users understand agreements and documents.

Answer the user's question using ONLY the document information provided below.

Rules:
- Give a short and direct answer.
- Start with the exact answer if possible.
- Use simple language.
- Maximum 3 short sentences.
- Do not repeat unnecessary parts of the document.
- Do not copy large portions of the document.
- Do not invent information.
- If the answer is not present in the provided information, say:
  "This information is not mentioned in the document."
- Do not provide legal advice.

Relevant document information:
{context}

User question:
{question}

Answer:
"""

    for attempt in range(2):

        try:

            interaction = client.interactions.create(
                model="gemini-3.6-flash",
                input=prompt
            )

            answer = interaction.output_text

            return {
                "answer": answer,
                "sources": relevant_chunks
            }

        except Exception as error:

            print("Gemini RAG error:", error)

            if is_rate_limit_error(error):

                return {
                    "answer": "Gemini API limit has been reached. Please try again later.",
                    "sources": []
                }

            if is_connection_error(error):

                if attempt == 0:
                    time.sleep(3)
                    continue

                return {
                    "answer": "Could not connect to the Gemini API. Please try again later.",
                    "sources": relevant_chunks
                }

            if attempt == 1:

                return {
                    "answer": "The Gemini API could not process the question right now.",
                    "sources": relevant_chunks
                }

            time.sleep(3)