from pydantic import BaseModel
from typing import List

class Section(BaseModel):
    name: str
    description: str
    research: bool
    content: str

class Report(BaseModel):
    sections: List[Section]