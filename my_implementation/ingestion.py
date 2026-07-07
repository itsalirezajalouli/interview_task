# externals 
import numpy as np
from rank_bm25 import BM25Okapi
from numpy.typing import NDArray
from typing_extensions import List, Tuple
from sentence_transformers import SentenceTransformer

# internals
from my_implementation.models import Document, Chunk
from my_implementation.recursive_chunking import recursive_chunking

# constants
CHUNK_SIZE = 400

def chunk_text(text, size=CHUNK_SIZE):
    # fixed-size character windows
    return [text[i:i + size] for i in range(0, len(text), size)]

def build_index_w_doc_model(
    docs: List[Document],
    model: SentenceTransformer
) -> Tuple[List[Chunk], NDArray[np.float64]]:

    chunks: List[Chunk] = []
    for d in docs:
        # for c in chunk_text(d.text):
        # after changin this, my implementation tests should still work: they do!
        for c in recursive_chunking(d.text):
            chunks.append(
                Chunk(
                    id = d.id,
                    title = d.title,
                    text = c
                )
            )
    vectors = model.encode([c.text for c in chunks])
    vectors = np.asarray(vectors, dtype = 'float32')
    vectors = vectors / np.linalg.norm(vectors, axis = 1, keepdims = True)
    return chunks, vectors

def build_bm25_index(chunks: List[Chunk]) -> BM25Okapi:
    corpus = [chunk.text.lower().split() for chunk in chunks]
    return BM25Okapi(corpus)
