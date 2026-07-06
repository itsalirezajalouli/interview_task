'''
This module has all the tests for RAG pipeline and we use it both for baseline
rag and for the solution we will implement afterwards, cause the evaluation
should be the same for 
'''

# internals
from baseline_rag import load_docs
from my_implementation.models import Document
from my_implementation.utils import load_docs_as_document
from evaluation.models import EvaluationTest

# TODO: I should expand the corpus! It's not challenging enough for the pipeline
# evaluation

baseline_docs = load_docs('corpus.jsonl')

extention = [
    # Let's spread information among 2 docs
    Document(
        id = 'DOC-17',
        title = 'Valve V-300 — Specifications',
        text = (
            'The V-300 is a pneumatically actuated control valve used on the '
            'cooling water return line. Valve size is DN80 with a flanged '
            'connection. Maximum allowable operating pressure is 10 bar. '
            'The actuator requires 6 bar instrument air to operate correctly. '
            'Fail-safe position on air loss is closed.'
        )
    ),
    Document(
        id = 'DOC-18',
        title = 'Valve V-300 — Inspection Requirements',
        text = (
            'For the V-300 control valve, inspect the actuator diaphragm and '
            'positioner every 6 months. Check seat leakage annually using the '
            'standard test procedure. Do not exceed the pressure rating stated '
            'in the equipment specification during leak testing. Lubricate the '
            'stem packing at each inspection and log the seat leakage result.'
        )
    ),
    Document(
        id = 'DOC-19',
        title = 'Compressor C-100 — Separator Element Replacement',
        text = (
            'The C-100 compressor undergoes extended maintenance checks beyond '
            'the standard schedule. Technicians should verify belt tension, '
            'inspect the intake filter for fouling, and confirm the control panel '
            'shows no active fault codes before proceeding with disassembly of the '
            'separator housing and the surrounding mounting brackets. '
            'The air-oil separator element on this unit should be replaced every 4000 op'
            # ------ here's where 400 chunk size breaks ------
            'erating hours to maintain separation efficiency. '
            'Log the replacement date and the part lot number in the maintenance '
            'record for traceability.'
        )
    )
]

EXTENDED_DOCS_FOR_BASELINE = baseline_docs + [e.model_dump() for e in extention]

my_pipeline_docs = load_docs_as_document('corpus.jsonl')
EXTENDED_DOCS_FOR_MY_PIPELINE = my_pipeline_docs + extention

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
            'The air-oil separator element on the C-100 should be replaced '
            'every 4000 operating hours.'
        )
    ),

}
