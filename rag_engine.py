# rag_engine.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ใช้ Model ตัวเล็กที่รองรับหลายภาษารวมถึงภาษาไทย
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class RAGEngine:
    def __init__(self, kb_path: str):
        self.model = SentenceTransformer(EMBED_MODEL)
        self.chunks = self._load_and_chunk(kb_path)
        self.index, self.embeddings = self._build_index()

    def _load_and_chunk(self, path: str) -> list[str]:
        """Load (ขั้นตอน 1) และ Chunk (ขั้นตอน 2)"""
        with open(path, encoding="utf-8") as f:
            text = f.read()
        return [c.strip() for c in text.split("\n\n") if c.strip()]

    def _build_index(self):
        """Embed (ขั้นตอน 3)"""
        embeddings = self.model.encode(self.chunks, show_progress_bar=False)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings, dtype="float32"))
        return index, embeddings

    def search(self, query: str, top_k: int = 3) -> list[str]:
        """Search (ขั้นตอน 4)"""
        q_emb = self.model.encode([query])
        _, indices = self.index.search(np.array(q_emb, dtype="float32"), top_k)
        return [self.chunks[i] for i in indices[0]]