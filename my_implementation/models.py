from pydantic import BaseModel, StrictStr

class Document(BaseModel):
    id: StrictStr
    title: StrictStr
    text: StrictStr


class Chunk(BaseModel):
    id: StrictStr
    title: StrictStr
    text: StrictStr
