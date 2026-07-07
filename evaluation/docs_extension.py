# internals
from baseline.baseline_rag import load_docs
from my_implementation.models import Document
from my_implementation.utils import load_docs_as_document

baseline_docs = load_docs('baseline/corpus.jsonl')

extension = [
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
    ),
    Document(
        id = 'DOC-20',
        title = 'Compressor C-100 — No-Start Conditions',
        text = (
            'The C-100 compressor must not be started if oil level is below '
            'the minimum sight glass mark, ambient temperature exceeds 45°C, '
            'or active fault codes are present on the control panel. '
            'Starting the C-100 compressor under any of these conditions '
            'will trigger an automatic shutdown.'
        )
    ),
    Document(
        id = 'DOC-21',
        title = 'Compressor C-100 — Startup Conditions',
        text = (
            'The C-100 compressor should only be started when all operating '
            'conditions are confirmed within range. Before starting the C-100 '
            'compressor, operators must verify that compressor start conditions '
            'are satisfied. Check all C-100 startup conditions before each '
            'start to confirm the unit is ready to run.'
        )
    ),
    Document(
        id = 'DOC-22',
        title = 'Error Code E-04 — Overtemperature Fault',
        text = (
            'Error code E-04 indicates the compressor discharge temperature '
            'has exceeded the safe operating limit. Check the cooling fan '
            'operation, inspect the oil cooler for blockage, and verify '
            'ambient temperature is within specification. The unit will not '
            'restart until temperature drops below the reset threshold and '
            'the fault is manually cleared.'
        )
    ),
    Document(
        id = 'DOC-23',
        title = 'Error Code E-05 — Low Oil Pressure Fault',
        text = (
            'Error code E-05 indicates oil pressure has dropped below the '
            'minimum operating threshold. Check the oil level in the sight '
            'glass, inspect the oil filter for blockage, and verify the oil '
            'pump is functioning. The unit will not restart until oil pressure '
            'is restored and the fault is manually cleared.'
        )
    ),
    Document(
        id = 'DOC-24',
        title = 'Compressor C-200 — Preliminary Overview',
        text = (
            'The C-200 is a new rotary screw compressor model currently in '
            'the product development pipeline. It builds on the C-100 platform '
            'with improved efficiency targets. Detailed specifications, '
            'performance data, and maintenance schedules will be published in '
            'a future service bulletin. For interim inquiries refer to the '
            'product management team.'
        )
    ),
]

EXTENDED_DOCS_FOR_BASELINE = baseline_docs + [e.model_dump() for e in extension]

my_pipeline_docs = load_docs_as_document('baseline/corpus.jsonl')
EXTENDED_DOCS_FOR_MY_PIPELINE = my_pipeline_docs + extension
