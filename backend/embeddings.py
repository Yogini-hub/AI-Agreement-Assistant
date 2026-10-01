from sklearn.feature_extraction.text import TfidfVectorizer


def create_embeddings(chunks):

    vectorizer = TfidfVectorizer()

    embeddings = vectorizer.fit_transform(chunks).toarray()

    return embeddings, vectorizer


def create_question_embedding(question, vectorizer):

    embedding = vectorizer.transform([question]).toarray()[0]

    return embedding