import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [documentText, setDocumentText] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    if (selectedFile.type !== "application/pdf") {
      setError("Please select a PDF file.");
      return;
    }

    setFile(selectedFile);
    setResult(null);
    setDocumentText("");
    setQuestion("");
    setAnswer("");
    setSources([]);
    setError("");
  };

  const analyzeDocument = async () => {
    if (!file) {
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setAnswer("");
    setSources([]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze document");
      }

      const data = await response.json();

      setResult(data.analysis);
      setDocumentText(data.text);
    } catch (error) {
      setError(
        "Something went wrong. Please make sure the backend is running."
      );
    }

    setLoading(false);
  };

  const askQuestion = async () => {
    if (!question.trim() || !documentText) {
      return;
    }

    setAsking(true);
    setAnswer("");
    setSources([]);
    setError("");

    const formData = new FormData();

    formData.append("document_text", documentText);
    formData.append("question", question);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to get answer");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setError(
        "Could not answer the question. Please make sure the backend is running."
      );
    }

    setAsking(false);
  };

  const exampleQuestions = [
    "What is the security deposit?",
    "When is the rent due?",
    "What is the notice period?",
  ];

  return (
    <div className="app">

      <div className="background-circle circle-one"></div>
      <div className="background-circle circle-two"></div>

      <header className="header">

        <div className="brand">
          <div className="brand-icon">AI</div>
          <span>DocumentLens</span>
        </div>

        <div className="header-badge">
          <span className="status-dot"></span>
          AI Document Assistant
        </div>

        <h1>
          Understand your documents
          <span> in seconds.</span>
        </h1>

        <p className="subtitle">
          Upload an agreement and let AI find important terms,
          financial details, obligations and clauses that deserve attention.
        </p>

      </header>

      <main className="main-content">

        <section className="upload-card">

          <div className="upload-top">

            <div className="document-icon">
              <span>PDF</span>
            </div>

            <div>
              <h2>Analyze a document</h2>

              <p>
                Upload a PDF agreement to get an easy-to-understand analysis.
              </p>
            </div>

          </div>

          <label className="drop-zone">

            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
            />

            <div className="upload-cloud">
              ↑
            </div>

            <h3>
              {file ? "Document selected" : "Drop your PDF here"}
            </h3>

            <p>
              {file
                ? file.name
                : "or click to browse from your computer"}
            </p>

            <span className="file-support">
              PDF files only
            </span>

          </label>

          {file && (
            <div className="selected-file">

              <div className="selected-file-icon">
                PDF
              </div>

              <div className="selected-file-info">
                <strong>{file.name}</strong>

                <span>
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </span>
              </div>

              <div className="file-check">
                ✓
              </div>

            </div>
          )}

          <button
            className="analyze-button"
            disabled={!file || loading}
            onClick={analyzeDocument}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing document...
              </>
            ) : (
              <>
                Analyze Document
                <span>→</span>
              </>
            )}
          </button>

          {error && (
            <div className="error-message">
              <span>!</span>
              {error}
            </div>
          )}

        </section>

        {result && (
          <section className="results-section">

            <div className="section-heading">

              <div>
                <span className="eyebrow">
                  ANALYSIS COMPLETE
                </span>

                <h2>
                  Document insights
                </h2>
              </div>

              <div className="success-badge">
                ✓ Analyzed
              </div>

            </div>

            <div className="summary-card">

              <div className="card-label">
                <span className="label-icon">
                  ✦
                </span>

                AI Summary
              </div>

              <p>
                {result.summary}
              </p>

            </div>

            <div className="results-grid">

              <div className="info-card">

                <div className="card-heading">

                  <div className="card-icon purple">
                    T
                  </div>

                  <div>
                    <h3>
                      Important Terms
                    </h3>

                    <span>
                      {result.important_terms.length} found
                    </span>
                  </div>

                </div>

                <ul>
                  {result.important_terms.map((item, index) => (
                    <li key={index}>
                      <span className="bullet"></span>
                      {item}
                    </li>
                  ))}
                </ul>

              </div>

              <div className="info-card">

                <div className="card-heading">

                  <div className="card-icon green">
                    ₹
                  </div>

                  <div>
                    <h3>
                      Financial Details
                    </h3>

                    <span>
                      {result.financial_details.length} found
                    </span>
                  </div>

                </div>

                <ul>
                  {result.financial_details.map((item, index) => (
                    <li key={index}>
                      <span className="bullet"></span>
                      {item}
                    </li>
                  ))}
                </ul>

              </div>

              <div className="info-card">

                <div className="card-heading">

                  <div className="card-icon blue">
                    D
                  </div>

                  <div>
                    <h3>
                      Important Dates
                    </h3>

                    <span>
                      {result.important_dates.length} found
                    </span>
                  </div>

                </div>

                <ul>
                  {result.important_dates.map((item, index) => (
                    <li key={index}>
                      <span className="bullet"></span>
                      {item}
                    </li>
                  ))}
                </ul>

              </div>

              <div className="info-card">

                <div className="card-heading">

                  <div className="card-icon orange">
                    ✓
                  </div>

                  <div>
                    <h3>
                      Obligations
                    </h3>

                    <span>
                      {result.obligations.length} found
                    </span>
                  </div>

                </div>

                <ul>
                  {result.obligations.map((item, index) => (
                    <li key={index}>
                      <span className="bullet"></span>
                      {item}
                    </li>
                  ))}
                </ul>

              </div>

            </div>

            <div className="attention-card">

              <div className="attention-header">

                <div className="warning-icon">
                  !
                </div>

                <div>
                  <h3>
                    Clauses to pay attention to
                  </h3>

                  <p>
                    These clauses may deserve a closer look.
                  </p>
                </div>

              </div>

              <div className="attention-list">

                {result.attention_clauses.map((item, index) => (
                  <div
                    className="attention-item"
                    key={index}
                  >
                    <span>
                      {index + 1}
                    </span>

                    <p>
                      {item}
                    </p>
                  </div>
                ))}

              </div>

            </div>

            <div className="question-section">

              <div className="question-header">

                <div>

                  <span className="eyebrow">
                    DOCUMENT Q&A
                  </span>

                  <h2>
                    Ask your document
                  </h2>

                  <p>
                    Ask a question and get a concise answer grounded
                    in the uploaded document.
                  </p>

                </div>

                <div className="rag-badge">
                  RAG enabled
                </div>

              </div>

              <div className="example-questions">

                <span>
                  Try asking:
                </span>

                {exampleQuestions.map((example, index) => (
                  <button
                    key={index}
                    onClick={() => setQuestion(example)}
                  >
                    {example}
                  </button>
                ))}

              </div>

              <div className="question-input-area">

                <input
                  type="text"
                  placeholder="Ask something about this document..."
                  value={question}
                  onChange={(event) =>
                    setQuestion(event.target.value)
                  }
                  onKeyDown={(event) => {
                    if (event.key === "Enter") {
                      askQuestion();
                    }
                  }}
                />

                <button
                  onClick={askQuestion}
                  disabled={!question.trim() || asking}
                >
                  {asking ? (
                    <span className="spinner"></span>
                  ) : (
                    "Ask"
                  )}
                </button>

              </div>

              {answer && (
                <div className="answer-area">

                  <div className="answer-header">

                    <div className="answer-ai-icon">
                      AI
                    </div>

                    <div>
                      <h3>
                        Answer
                      </h3>

                      <span>
                        Based on your document
                      </span>
                    </div>

                  </div>

                  <p className="answer-text">
                    {answer}
                  </p>

                  {sources.length > 0 && (
                    <div className="sources-section">

                      <div className="sources-title">
                        <span>⌕</span>
                        Relevant document sections
                      </div>

                      <div className="source-list">

                        {sources.slice(0, 2).map((source, index) => (
                          <div
                            className="source-item"
                            key={index}
                          >

                            <span className="source-number">
                              {index + 1}
                            </span>

                            <p>
                              {source}
                            </p>

                          </div>
                        ))}

                      </div>

                    </div>
                  )}

                </div>
              )}

            </div>

          </section>
        )}

        {!result && !loading && (
          <div className="features">

            <div className="feature">

              <div className="feature-icon">
                ✦
              </div>

              <h3>
                Smart Analysis
              </h3>

              <p>
                Extract important information automatically.
              </p>

            </div>

            <div className="feature">

              <div className="feature-icon">
                ⌕
              </div>

              <h3>
                Ask Questions
              </h3>

              <p>
                Ask questions using natural language.
              </p>

            </div>

            <div className="feature">

              <div className="feature-icon">
                ✓
              </div>

              <h3>
                Grounded Answers
              </h3>

              <p>
                Answers are based on relevant document sections.
              </p>

            </div>

          </div>
        )}

      </main>

      <footer>

        <p>
          AI Agreement & Document Risk Assistant
        </p>

        <span>
          For informational purposes only — not legal advice.
        </span>

      </footer>

    </div>
  );
}

export default App;