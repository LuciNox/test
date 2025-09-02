from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

from .answer import AnswersTable

class Question(SQLModel):
    text: str = Field(default=None)

class QuestionsTable(Question, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.today)

    answer: Optional[AnswersTable] = Relationship(cascade_delete=True)