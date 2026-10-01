# AI Agreement & Document Risk Assistant

An AI-powered document assistant that helps users understand agreements by extracting important information, identifying clauses that may require attention, and answering questions based on the uploaded document.

The application is designed for documents such as rental agreements, hostel agreements, internship agreements, service agreements, and similar documents.

## Live Demo

https://ai-agreement-assistant.vercel.app/

## GitHub Repository

https://github.com/Yogini-hub/AI-Agreement-Assistant

---

## Overview

Understanding long agreements can be difficult because important information is often spread across multiple sections.

The **AI Agreement & Document Risk Assistant** makes this easier by allowing users to upload a PDF and receive a structured analysis of the document.

The application can:

- Summarize the document
- Extract important terms
- Identify financial details
- Extract important dates
- Identify obligations
- Highlight clauses that may require attention
- Answer questions about the uploaded document
- Show relevant sections used to answer questions

The system uses **Retrieval-Augmented Generation (RAG)** so that questions are answered using relevant sections from the uploaded document.

---

## Features

### PDF Document Upload

Users can upload an agreement in PDF format.

### Document Summary

The application generates a simple summary of the uploaded document.

### Important Terms

Important information such as:

- Parties involved
- Agreement type
- Duration
- Notice period
- Deposit
- Other important conditions

can be extracted from the document.

### Financial Details

The application identifies financial information such as:

- Rent
- Security deposit
- Fees
- Penalties
- Other payments

### Important Dates

The system extracts relevant dates and deadlines mentioned in the agreement.

### Obligations

The application identifies important responsibilities and obligations mentioned in the document.

### Attention Clauses

Potentially important clauses are highlighted so users know which sections deserve closer attention.

### Document Q&A

Users can ask questions about the uploaded agreement.

For example:

- What is the security deposit?
- What is the notice period?
- When should the rent be paid?
- What are the tenant's responsibilities?
- Are there any penalties mentioned?

The system retrieves relevant document sections before generating an answer.

---

## How It Works

The application follows a simple document processing and RAG pipeline.

```text
                 User
                  |
                  v
            Upload PDF
                  |
                  v
        Extract PDF Text
                  |
                  v
          Split into Chunks
                  |
                  v
       Create Document Index
                  |
                  v
        Gemini Document Analysis
                  |
                  v
        Display Structured Results
                  |
                  v
             User Question
                  |
                  v
       Retrieve Relevant Chunks
                  |
                  v
          Gemini + Context
                  |
                  v
          Answer + Sources
