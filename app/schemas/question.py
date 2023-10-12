from datetime import datetime

from pydantic import BaseModel


class QuestionDB(BaseModel):
    id: int
    question_text: str
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True
