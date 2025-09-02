from datetime import datetime
from sqlmodel import Field, SQLModel

class Answer(SQLModel):
    question_id: int = Field(default=None, foreign_key="questionstable.id", ondelete="CASCADE")
    text: str = Field(default=None)

class AnswersTable(Answer, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.today)