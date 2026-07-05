from typing_extensions import List, Literal
from pydantic import BaseModel, StrictStr, StrictInt


class EvaluationTest(BaseModel):
    idx: StrictInt

    user_query: StrictStr
    retrieved_docs: List[StrictStr] # List of document ids (names)

    expected_behaviour: Literal['answer', 'abstain']
    expected_behaviour_docs: List[StrictStr]
    expected_behaviour_answer: StrictStr | None


class EvaluationResult(BaseModel):
    test_idx: StrictInt

    retrieved_docs: List[StrictStr] # List of document ids (names)
    hit: bool # Was actual doc in retrieved_docs? 
    actual_behavior: Literal['answer', 'abstain']

    passed: bool
