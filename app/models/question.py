from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)

from app.core.db import Base


class Question(Base):
    id = Column(Integer, primary_key=True)
    question_text = Column(Text, unique=True)
    answer = Column(String(200), nullable=False)
    created_at = Column(DateTime)
    downloaded_at = Column(DateTime)
