# externals
import unittest
from sentence_transformers import SentenceTransformer

# internals
from baseline_rag import build_index, answer
from evaluation.tests import TEST_SUIT, EXTENDED_DOCS_FOR_BASELINE

class BaselineEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: later will import load_extended_docs from evaluation.tests
        self.docs = EXTENDED_DOCS_FOR_BASELINE
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks, self.vectors = build_index(self.docs, self.model)
        self.score_threshold = 0.30 # I might change this, no reason for this number

    # Correctness
    def test01_single_doc_direct_query(self):
        query = TEST_SUIT['t01_single_doc_direct_query'].user_query
        expected_docs = TEST_SUIT['t01_single_doc_direct_query'].expected_docs
        expected_answer = TEST_SUIT['t01_single_doc_direct_query'].expected_answer
        chunk, score = answer(query, self.chunks, self.vectors, self.model)

        self.assertIn(
            chunk['doc_id'], # type: ignore
            expected_docs,
            'Retrieved document should be in expected documents.'
        )

        self.assertIn(
            expected_answer,
            chunk['text'],# type: ignore
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
            len([chunk]),
            len(expected_docs),
            'Number of retrieved documents should equal to expected documents.',
        )


    # Retrieval recall or coverage
    def test02_multi_doc_direct_query(self):
        query = TEST_SUIT['t02_multi_doc_direct_query'].user_query
        expected_docs = TEST_SUIT['t02_multi_doc_direct_query'].expected_docs
        chunk, _ = answer(query, self.chunks, self.vectors, self.model)

        self.assertIn(
            chunk['doc_id'], # type: ignore
            expected_docs,
            'Retrieved document should be in expected documents.'
        )

        self.assertEqual(
            len([chunk]),
            len(expected_docs),
            'Number of retrieved documents should equal to expected documents.',
        )
