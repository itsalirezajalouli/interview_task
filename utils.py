import json
from typing_extensions import List
from pydantic import BaseModel, StrictStr

class Document(BaseModel):
    id: StrictStr
    title: StrictStr
    text: StrictStr

def load_docs(path: StrictStr) -> List[Document]:
    docs = []
    with open(path, encoding="utf-8") as f:
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

if __name__ == '__main__':
    docs = load_docs('corpus.jsonl')
    for d in docs: 
        print(d.title)
