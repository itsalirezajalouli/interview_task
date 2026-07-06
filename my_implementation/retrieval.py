# externals
import numpy as np
from numpy.typing import NDArray
from typing_extensions import List
from pydantic import StrictFloat, StrictStr, StrictInt
from sentence_transformers import SentenceTransformer

# internals
from my_implementation.models import Chunk

def retrieve(
    query: StrictStr,
    chunks: List[Chunk],
    vectors: NDArray[np.float64],
    model: SentenceTransformer,
    threshold: StrictFloat,
    top_k: StrictInt = 5,
):
    q = model.encode([query])[0].astype("float32") # type: ignore
    q = q / np.linalg.norm(q)
    sims = vectors @ q

    # here's the first point we diverge in implementation
    ind = np.argpartition(sims, -top_k)[-top_k:][::-1]

    best_chunks_w_scores = [
        (chunks[int(x)], float(sims[x])) for x in ind if sims[x] > threshold
    ]

    return best_chunks_w_scores


def answer_w_topk(
    query: StrictStr,
    chunks: List[Chunk],
    vectors: NDArray[np.float64],
    model: SentenceTransformer,
    threshold: StrictFloat,
):
    hit = retrieve(query, chunks, vectors, model, threshold)
    # returns the best-matching chunks not just one chunk
    return hit
    # return f"[{hit['doc_id']} | {score:3f}] {hit.text}"
