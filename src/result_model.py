from pydantic import BaseModel
from typing import List


class ResultModel(BaseModel):
    elective_title: str
    short_description: str
    full_description: str
    elective_author: str
    author_description: str
    elective_tags: List[str] = None
    minor: str = None
