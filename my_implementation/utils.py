# externals 
import json
from pydantic import StrictStr
from typing_extensions import List

# internals
from my_implementation.models import Document


def load_docs_as_document(path: StrictStr) -> List[Document]:
    docs = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                # Added a simple validation because you mentioned we should 
                # count for industrial environment data inconsistency.
                # In this cases, better to have a data model and a 
                # validation layer.
                docs.append(
                    Document.model_validate(json.loads(line))
                )
    return docs

