from typing import List, Dict, Union
from pydantic import BaseModel


class TranslationPost(BaseModel):
    text: str
    languages: List[str]


class TaskResponse(BaseModel):
    task_id: Union[str, int]


class TranslationStatus(BaseModel):
    task_id: Union[str, int]
    status: str
    text: str
    translation: List
