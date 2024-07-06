from sqlalchemy import Column, Integer, Text, JSON, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TranslationTask(Base):
    __tablename__ = "translation_task"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    languages = Column(JSON, nullable=False)
    status = Column(VARCHAR(100), nullable=False, default="ongoing")
    translation = Column(JSON, nullable=False, default=[])
