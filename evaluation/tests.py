'''
This module has all the tests for RAG pipeline and we use it both for baseline
rag and for the solution we will implement afterwards, cause the evaluation
should be the same for 
'''

# internals
from evaluation.models import EvaluationTest

TEST_SUIT = {
    # Correctness
    't01_single_doc_direct_query': EvaluationTest(
        idx = 1,
        user_query = 'What is BRG-4410?',
        expected_behaviour = 'answer',
        expected_docs = ['DOC-09'],
        expected_answer = (
            'The BRG-4410 is a sealed deep-groove ball bearing used on several '
            'fan and motor assemblies.'
        )
    ),

    # Recall
    't02_multi_doc_direct_query': EvaluationTest(
        idx = 2,
        user_query = 'What is the maximum operating pressure of the V-300 valve, and how often should it be inspected?',
        expected_behaviour = 'answer',
        expected_docs = ['DOC-18', 'DOC-17'],
        expected_answer = (
            'The V-300 has a maximum allowable operating pressure of 10 bar '
            '(DOC-16). Its actuator diaphragm and positioner should be '
            'inspected every 6 months, with seat leakage checked annually '
            '(DOC-17).'
        )
    ),

    # Precison
    't03_multi_chunk_direct_query': EvaluationTest(
        idx = 3,
        user_query = "How often should the C-100's air-oil separator element be replaced?",
        expected_behaviour = 'answer',
        expected_docs = ['DOC-19'],
        expected_answer = (
            'The air-oil separator element on this unit should be replaced '
            'every 4000 operating hours to maintain separation efficiency. '
        )
    ),

    # Ranking Quality (MRR)
    't04_negation_direct_query': EvaluationTest(
        idx = 4,
        user_query = 'Under what conditions should the C-100 compressor not be started?',
        expected_behaviour = 'answer',
        expected_docs = ['DOC-20'],
        expected_answer = (
            'The C-100 compressor must not be started if oil level is below '
            'the minimum sight glass mark, ambient temperature exceeds 45°C, '
            'or active fault codes are present on the control panel. '
        )
    ),

    # Lexical Precision
    't05_exact_code__direct_query': EvaluationTest(
        idx = 5,
        user_query = 'What does error code E-04 indicate?',
        expected_behaviour = 'answer',
        expected_docs = ['DOC-22'],
        expected_answer = (
            ''
        )
    ),

    # Abstain — in-domain, not in corpus
    't06_abstain_in_domain': EvaluationTest(
        idx = 6,
        user_query = 'What is the oil change interval for the C-100 compressor?',
        expected_behaviour = 'abstain',
        expected_docs = [],
        expected_answer = None,
    ),

    # Abstain — near-miss (C-200 exists but no specs)
    't07_abstain_near_miss': EvaluationTest(
        idx = 7,
        user_query = 'What is the rated output of the C-200 compressor?',
        expected_behaviour = 'abstain',
        expected_docs = [],
        expected_answer = None,
    ),

    # Abstain — out-of-domain
    't08_abstain_out_of_domain': EvaluationTest(
        idx = 8,
        user_query = 'What is the recommended tire pressure for the warehouse forklift?',
        expected_behaviour = 'abstain',
        expected_docs = [],
        expected_answer = None,
    ),
}
