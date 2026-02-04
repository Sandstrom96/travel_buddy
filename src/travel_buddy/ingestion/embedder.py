from sentence_transformers import SentenceTransformer
from travel_buddy.utils.settings import settings


class EmbeddingService:
    def __init__(self):
        print(f"Loading embedding model: {settings.embedding_model}")
        self.model = SentenceTransformer(settings.embedding_model)

    def embed_chunks(self, chunks: list[dict]) -> list[dict]:
        texts = [chunk['text'] for chunk in chunks]

        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)

        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding.tolist()

        return chunks