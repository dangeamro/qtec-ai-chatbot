import faiss
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunks = []

    def chunk_text(self, text, chunk_size=1000, overlap=200):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunks.append(" ".join(words[i:i + chunk_size]))
        return chunks

    def add_document(self, text):
        new_chunks = self.chunk_text(text)
        self.chunks.extend(new_chunks)
        embeddings = self.model.encode(self.chunks)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve(self, query, k=3):
        if self.index is None:
            return []
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        return [self.chunks[i] for i in indices[0]]

retriever = Retriever()