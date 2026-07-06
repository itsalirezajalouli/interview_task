# externals 
import numpy as np
from numpy.typing import NDArray
from typing_extensions import List, Tuple
from sentence_transformers import SentenceTransformer

# internals
from my_implementation.models import Document, Chunk

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
        for c in chunk_text(d.text):
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

