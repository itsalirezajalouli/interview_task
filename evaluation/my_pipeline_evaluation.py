# externals
import unittest
from sentence_transformers import SentenceTransformer

# internals
from my_implementation.ingestion import build_index_w_doc_model
from my_implementation.retrieval import answer_w_topk
from evaluation.tests import TEST_SUIT, EXTENDED_DOCS_FOR_MY_PIPELINE

class MyImplementationEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: later will import load_extended_docs from evaluation.tests
        self.docs = EXTENDED_DOCS_FOR_MY_PIPELINE
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks, self.vectors = build_index_w_doc_model(self.docs, self.model)
        self.score_threshold = 0.6 # I might change this, no reason for this number

    # Correctness
    def test01_single_doc_direct_query(self):
        query = TEST_SUIT['t01_single_doc_direct_query'].user_query
        expected_docs = TEST_SUIT['t01_single_doc_direct_query'].expected_docs
        expected_answer = TEST_SUIT['t01_single_doc_direct_query'].expected_answer

        chunks = answer_w_topk(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.score_threshold
        )

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
                self.score_threshold,
                f'Retrieved answer score should be greater or equal to {self.score_threshold}.'
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

        chunks = answer_w_topk(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.score_threshold
        )

        self.assertEqual(
            len(chunks),
            len(expected_docs),
            'Number of retrieved documents should equal to expected documents.',
        )

        for chunk, score in chunks: 
            self.assertGreaterEqual(
                score,
                self.score_threshold,
                f'Retrieved answer score should be greater or equal to {self.score_threshold}.'
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

        chunks = answer_w_topk(
            query,
            self.chunks,
            self.vectors,
            self.model,
            self.score_threshold
        )

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
                self.score_threshold,
                f'Retrieved answer score should be greater or equal to {self.score_threshold}.'
            )
