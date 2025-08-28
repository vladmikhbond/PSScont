from pydantic import BaseModel
from datetime import datetime

class ProblemPostSchema(BaseModel):
    title: str
    attr: str
    lang: str
    cond: str
    view: str
    hint: str
    code: str
    author: str

    class Config:
        # orm_mode = True
        from_attributes=True

class ProblemSchema(ProblemPostSchema):
    id: str

    class Config:
        # orm_mode = True
        from_attributes=True
        

class CheckSchema(BaseModel):
    id: str
    solving: str

class ProofSchema(BaseModel):
    source: str
    lang: str

   
