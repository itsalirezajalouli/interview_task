from typing_extensions import List, Literal
from pydantic import BaseModel, StrictStr, StrictInt


class EvaluationTest(BaseModel):
    idx: StrictInt

    user_query: StrictStr
    # I had retrieved_docs here which makes no sense for a test,
    # moved it to result

    # also these names made no sense, fixed them
    expected_behaviour: Literal['answer', 'abstain']
    expected_docs: List[StrictStr]
    expected_answer: StrictStr | None
