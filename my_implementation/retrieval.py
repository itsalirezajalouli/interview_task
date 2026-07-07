# externals
import numpy as np
from rank_bm25 import BM25Okapi
from numpy.typing import NDArray
from typing_extensions import List, Tuple
from pydantic import StrictFloat, StrictStr, StrictInt
from sentence_transformers import SentenceTransformer, CrossEncoder

# internals
from my_implementation.models import Chunk

def retrieve(
    query: StrictStr,
    chunks: List[Chunk],
    vectors: NDArray[np.float64],
    model: SentenceTransformer,
    threshold: StrictFloat,
    top_k: StrictInt = 5,
) -> List[Tuple[Chunk, float]]:
    q = model.encode([query])[0].astype("float32") # type: ignore
    q = q / np.linalg.norm(q)
    sims = vectors @ q

    # here's the first point we diverge in implementation
    ind = np.argpartition(sims, -top_k)[-top_k:][::-1]

    return [
        (chunks[int(x)], float(sims[x])) for x in ind if sims[x] > threshold
    ]


def rerank(
    query: StrictStr,
    candidates: List[Tuple[Chunk, float]],
    reranker: CrossEncoder,
) -> List[Tuple[Chunk, float]]:
    chunks = [chunk for chunk, _ in candidates]
    scores = reranker.predict([(query, chunk.text) for chunk in chunks])

    # argsort returns the indexes that sort the array, not the values
    ordered_inds = np.argsort(scores)[::-1]
    return [(chunks[i], float(scores[i])) for i in ordered_inds]

# baseline test needs this so we won't break backward compatability
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

def answer_w_rerank(
    query: StrictStr,
    chunks: List[Chunk],
    vectors: NDArray[np.float64],
    model: SentenceTransformer,
    reranker: CrossEncoder,
    threshold: StrictFloat,
):
    retrieved_chunks = retrieve(
        query,
        chunks,
        vectors,
        model,
        threshold
    )

    # returns the best-matching chunkS RERANKED!
    reranked_chunks = rerank(query, retrieved_chunks, reranker)

    return reranked_chunks

def normalize_dense_scores(scores: NDArray):
    lo, hi = scores.min(), scores.max()
    return (scores - lo) / (hi - lo) if hi != lo else np.zeros_like(scores)


def hybrid_retrieve(
    query: StrictStr,
    chunks: List[Chunk],
    vectors: NDArray[np.float64],
    model: SentenceTransformer,
    bm25: BM25Okapi,
    top_k: StrictInt = 5,
    alpha: float = 0.5, # this sets the mix ratio between bm25 and cosine similarity(semantic search)
) -> List[Tuple[Chunk, float]]:
    # same as before
    q = model.encode([query])[0].astype('float32')
    q = q / np.linalg.norm(q)
    dense_scores = vectors @ q

    # new
    bm25_scores = np.array(bm25.get_scores(query.lower().split()))
    hybrid_scores = alpha * normalize_dense_scores(dense_scores) + (1 - alpha) * normalize_dense_scores(bm25_scores)

    ordered_ind = np.argpartition(hybrid_scores, -top_k)[-top_k:][::-1]
    return [
        (chunks[int(i)], float(hybrid_scores[i])) for i in ordered_ind
    ]
