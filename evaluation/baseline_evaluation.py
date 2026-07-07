# externals
import unittest
from sentence_transformers import SentenceTransformer

# internals
from baseline_rag import build_index, answer
from evaluation.tests import (
    TEST_SUIT,
    EXTENDED_DOCS_FOR_BASELINE,
    EXTENDED_DOCS_FOR_MY_PIPELINE,
)
from my_implementation.retrieval import answer_w_topk
from my_implementation.ingestion import build_index_w_doc_model

class BaselineEvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: later will import load_extended_docs from evaluation.tests
        self.docs = EXTENDED_DOCS_FOR_BASELINE
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks, self.vectors = build_index(self.docs, self.model)
        # threshold is useless in this pipline cause we only get the argmax anyway

    # Correctness
    def test01_single_doc_direct_query(self):
        query = TEST_SUIT['t01_single_doc_direct_query'].user_query
        expected_docs = TEST_SUIT['t01_single_doc_direct_query'].expected_docs
        expected_answer = TEST_SUIT['t01_single_doc_direct_query'].expected_answer

        chunk, score = answer(
            query,
            self.chunks,
            self.vectors,
            self.model
        )

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

        self.assertEqual(
            len([chunk]),
            len(expected_docs),
            'Number of retrieved documents should equal to expected documents.',
        )


    # Retrieval recall or coverage: supposed to fail
    def test02_multi_doc_direct_query(self):
        query = TEST_SUIT['t02_multi_doc_direct_query'].user_query
        expected_docs = TEST_SUIT['t02_multi_doc_direct_query'].expected_docs

        chunk, _ = answer(
            query,
            self.chunks,
            self.vectors,
            self.model
        )

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

    # Percision
    def test03_multi_chunk_direct_query(self):
        query = TEST_SUIT['t03_multi_chunk_direct_query'].user_query
        expected_docs = TEST_SUIT['t03_multi_chunk_direct_query'].expected_docs
        expected_answer = TEST_SUIT['t03_multi_chunk_direct_query'].expected_answer

        # NOTE: For this test this pipeline will fail conceptually because it
        # can't return more than one document.
        # We imagine the previous bug got fixed. I let baseline
        # use my own implementation of answer function

        # kinda new startup because we imagined that bug didn't exist
        chunks, vectors = build_index_w_doc_model(
            EXTENDED_DOCS_FOR_MY_PIPELINE,
            self.model
        )
        answer = answer_w_topk(
            query,
            chunks,
            vectors,
            self.model,
            0.3 # let's be generous and see when "DOC-19-chunk-2" appears in the list
        )

        # print(answer)
        # I printed to see where in the results "DOC-19-chunk-2" appears:
        # ['DOC-19'(chunk 1), 'DOC-03', 'DOC-12', 'DOC-19'(chunk 1)]
        for chunk, score in answer:
            self.assertIn(
                chunk.id,
                expected_docs,
                'Retrieved documents should match expected documents.'
            )
            self.assertEqual(
                chunk.text,
                expected_answer,
                'Retrieved document content should match expected document content exactly'
            )

    # Ranking Quality (MRR)
    def test04_negation_direct_query(self):
        query = TEST_SUIT['t04_negation_direct_query'].user_query
        expected_docs = TEST_SUIT['t04_negation_direct_query'].expected_docs

        chunk, _ = answer(
            query,
            self.chunks,
            self.vectors,
            self.model
        )

        self.assertIn(
            chunk['doc_id'], # type: ignore
            expected_docs,
            'Retrieved document should be in expected documents.'
        )

        # this is how i measured MRR but didn't clean up to show how i
        # found it out
        #chunks, vectors = build_index_w_doc_model(
        #    EXTENDED_DOCS_FOR_MY_PIPELINE,
        #    self.model
        #)
        #answerz = answer_w_topk(
        #    query,
        #    chunks,
        #    vectors,
        #    self.model,
        #    0.3 # let's be generous and see when "DOC-19-chunk-2" appears in the list
        #)

        # just to measure MRR
        #print(answerz)
        # MRR = 1/5! amazing XD

    # Lexical Precision
    def test05_exact_code__direct_query(self):
        query = TEST_SUIT['t05_exact_code__direct_query'].user_query
        expected_docs = TEST_SUIT['t05_exact_code__direct_query'].expected_docs

        chunks, vectors = build_index_w_doc_model(
            EXTENDED_DOCS_FOR_MY_PIPELINE,
            self.model
        )
        answer = answer_w_topk(
            query,
            chunks,
            vectors,
            self.model,
            0.6
        )
        retrieved_docs = [c.id for c, _ in answer]
        self.assertEqual(
            retrieved_docs,
            expected_docs,
            'Retrieved document should be in expected documents.'
        )
