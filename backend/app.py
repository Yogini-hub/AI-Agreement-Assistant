from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from pdf_reader import extract_text_from_pdf
from gemini_service import analyze_document, answer_with_rag
from rag_service import create_document_index, retrieve_relevant_chunks


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Stores the current document's chunks and embeddings
document_index = None


@app.get("/")
def home():
    return {
        "message": "AI Agreement Assistant Backend is running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    global document_index

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text from PDF
    text = extract_text_from_pdf(file_path)

    # Ask Gemini to analyze the document
    analysis = analyze_document(text)

    # Create chunks and embeddings only once
    document_index = create_document_index(text)

    return {
        "filename": file.filename,
        "text": text,
        "analysis": analysis
    }


@app.post("/ask")
async def ask_about_document(
    document_text: str = Form(...),
    question: str = Form(...)
):

    if document_index is None:
        return {
            "answer": "Please upload and analyze a document first.",
            "sources": []
        }

    # Search the already-created document embeddings
    relevant_chunks = retrieve_relevant_chunks(
        document_index,
        question
    )

    # Ask Gemini using only the relevant chunks
    result = answer_with_rag(
        question,
        relevant_chunks
    )

    return result