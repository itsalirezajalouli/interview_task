# externals
import unittest
from sentence_transformers import SentenceTransformer, CrossEncoder

# internals
from my_implementation.retrieval import hybrid_retrieve, rerank
# NOTE: answer_w_rerank replaced by hybrid_retrieve + rerank for all tests
# from my_implementation.retrieval import answer_w_rerank, hybrid_retrieve
from evaluation.tests import TEST_SUIT
from evaluation.docs_extension import EXTENDED_DOCS_FOR_MY_PIPELINE
from my_implementation.ingestion import build_index_w_doc_model, build_bm25_index

class MyImplementationEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.docs = EXTENDED_DOCS_FOR_MY_PIPELINE
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.chunks, self.vectors = build_index_w_doc_model(self.docs, self.model)
        # NOTE: threshold moved inline per-test so each test can tune independently
        # self.score_threshold = 0.6
        self.bm25 = build_bm25_index(self.chunks)

    # Correctness
    def test01_single_doc_direct_query(self):
        query = TEST_SUIT['t01_single_doc_direct_query'].user_query
        expected_docs = TEST_SUIT['t01_single_doc_direct_query'].expected_docs
        expected_answer = TEST_SUIT['t01_single_doc_direct_query'].expected_answer

        # NOTE: hybrid_retrieve + rerank replaces answer_w_rerank; threshold applied inline
        # chunks = answer_w_rerank(
        #     query,
        #     self.chunks,
        #     self.vectors,
        #     self.model,
        #     self.reranker,
        #     self.score_threshold
        # )
        threshold = 0.6
        candidates = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
        )
        chunks = rerank(query, candidates, self.reranker)
        chunks = [(c, s) for c, s in chunks if s >= threshold]

        for chunk, score in chunks: 
            self.assertIn(
                chunk.id,
                expected_docs,
                'Retrieved document should be in expected documents.'
            )

            self.assertIn(
                expected_answer,
                chunk.text,
                'Retrieved answer string should include expected answer.'
            )

            # This is experimental, I want to see what score threshold can 
            # ensure relevancy of the documents
            self.assertGreaterEqual(
                score,
                threshold,
                f'Retrieved answer score should be greater or equal to {threshold}.'
            )

            self.assertEqual(
                len(chunks),
                len(expected_docs),
                'Number of retrieved documents should equal to expected documents.',
            )

    # Retrieval recall or coverage
    def test02_multi_doc_direct_query(self):
        query = TEST_SUIT['t02_multi_doc_direct_query'].user_query
        expected_docs = TEST_SUIT['t02_multi_doc_direct_query'].expected_docs

        # NOTE: hybrid_retrieve + rerank replaces answer_w_rerank; threshold applied inline
        # chunks = answer_w_rerank(
        #     query,
        #     self.chunks,
        #     self.vectors,
        #     self.model,
        #     self.reranker,
        #     self.score_threshold
        # )
        threshold = 0.7
        candidates = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
        )
        chunks = rerank(query, candidates, self.reranker)
        chunks = [(c, s) for c, s in chunks if s >= threshold]

        self.assertEqual(
            len(chunks),
            len(expected_docs),
            'Number of retrieved documents should equal to expected documents.',
        )

        for chunk, score in chunks: 
            self.assertGreaterEqual(
                score,
                threshold,
                f'Retrieved answer score should be greater or equal to {threshold}.'
            )

            self.assertIn(
                chunk.id,
                expected_docs,
                'Retrieved documents should be in expected documents.'
            )

    # Precision
    def test03_multi_chunk_direct_query(self):
        query = TEST_SUIT['t03_multi_chunk_direct_query'].user_query
        expected_docs = TEST_SUIT['t03_multi_chunk_direct_query'].expected_docs
        expected_answer = TEST_SUIT['t03_multi_chunk_direct_query'].expected_answer

        # NOTE: hybrid_retrieve + rerank replaces answer_w_rerank; threshold applied inline
        # chunks = answer_w_rerank(
        #     query,
        #     self.chunks,
        #     self.vectors,
        #     self.model,
        #     self.reranker,
        #     self.score_threshold
        # )
        threshold = 1.7
        candidates = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
        )
        chunks = rerank(query, candidates, self.reranker)
        chunks = [(c, s) for c, s in chunks if s >= threshold]

        for chunk, score in chunks: 
            self.assertEqual(
                [chunk.id],
                expected_docs,
                'Retrieved document should be equal expected document.'
            )
            self.assertEqual(
                chunk.text,
                expected_answer,
                'Retrieved document content should match expected document content exactly'
            )
            self.assertGreaterEqual(
                score,
                threshold,
                f'Retrieved answer score should be greater or equal to {threshold}.'
            )

    # Ranking Quality (MRR)
    def test04_negation_direct_query(self):
        query = TEST_SUIT['t04_negation_direct_query'].user_query
        expected_docs = TEST_SUIT['t04_negation_direct_query'].expected_docs
        expected_answer = TEST_SUIT['t04_negation_direct_query'].expected_answer

        # NOTE: hybrid_retrieve + rerank replaces answer_w_rerank; threshold applied inline
        # ranked_chunks = answer_w_rerank(
        #     query,
        #     self.chunks,
        #     self.vectors,
        #     self.model,
        #     self.reranker,
        #     self.score_threshold
        # )
        threshold = 0.6
        candidates = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
        )
        ranked_chunks = rerank(query, candidates, self.reranker)
        ranked_chunks = [(c, s) for c, s in ranked_chunks if s >= threshold]

        first_candidate, _ = ranked_chunks[0]

        self.assertEqual(
            [first_candidate.id],
            expected_docs,
            'Retrieved document should be equal expected document.'
        )

        self.assertEqual(
            first_candidate.text,
            expected_answer,
            'Retrieved document content should match expected document content exactly'
        )

    # Lexical Precision
    def test05_exact_code__direct_query(self):

        query = TEST_SUIT['t05_exact_code__direct_query'].user_query
        expected_docs = TEST_SUIT['t05_exact_code__direct_query'].expected_docs

        # NOTE: hybrid_retrieve replaces pure dense/bi-encoder to fix lexical
        # precision; BM25 boosts exact token match (e-04) over similar codes (e-05).
        retrieved_chunks = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
        )

        # Verify top result is DOC-22 with normalized score 1.0
        top_chunk, top_score = retrieved_chunks[0]
        self.assertEqual(
            [top_chunk.id],
            expected_docs,
            'Top retrieved document should be the expected document.',
        )
        self.assertEqual(
            top_score,
            1.0,
            'Top retrieved document should have a normalized hybrid score of 1.0.',
        )

    # Abstain — in-domain, not in corpus
    def test06_abstain_in_domain(self):
        query = TEST_SUIT['t06_abstain_in_domain'].user_query

        # "oil change" never appears in corpus so top hybrid score peaks at 0.88
        # catching it here means we never waste time reranking
        candidates = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
            abstain_threshold=0.9,
        )
        chunks = rerank(query, candidates, self.reranker) if candidates else []

        self.assertEqual(
            chunks,
            [],
            'Pipeline should abstain but returned results.',
        )

    # Abstain — near-miss 
    def test07_abstain_near_miss(self):
        query = TEST_SUIT['t07_abstain_near_miss'].user_query

        # "rated output" appears in DOC-03 giving it a perfect hybrid
        # score (1.0), so hybrid threshold can't save us here. Reranker sees
        # it and scores DOC-03 at 7.5
        candidates = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
        )
        chunks = rerank(query, candidates, self.reranker) if candidates else []
        chunks = [(c, s) for c, s in chunks if s >= 8.0]

        self.assertEqual(
            chunks,
            [],
            'Pipeline should abstain but returned results.',
        )

    # Abstain — out-of-domain
    def test08_abstain_out_of_domain(self):
        query = TEST_SUIT['t08_abstain_out_of_domain'].user_query

        # "pressure" appears everywhere in this corpus so hybrid scores are high
        # can't abstain at hybrid level, but reranker scores everything negative
        candidates = hybrid_retrieve(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.bm25,
        )
        chunks = rerank(query, candidates, self.reranker) if candidates else []
        chunks = [(c, s) for c, s in chunks if s >= 0.0]

        self.assertEqual(
            chunks,
            [],
            'Pipeline should abstain but returned results.',
        )
