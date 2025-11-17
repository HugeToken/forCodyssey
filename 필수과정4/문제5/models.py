# models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Question(Base):
    """
    질문 모델 (Question Model)
    """
    __tablename__ = 'question'

    # 질문id: 질문 데이터의 고유번호 (primary key)
    id = Column(Integer, primary_key=True, index=True) 
    # subject: 질문 제목
    subject = Column(String(200), nullable=False)
    # content: 질문 내용
    content = Column(Text, nullable=False)
    # create_date: 질문 작성일시
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    
    # Answer 모델과의 관계 정의 (역참조)
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    """
    답변 모델 (Answer Model)
    """
    __tablename__ = 'answer'

    # 답변 id
    id = Column(Integer, primary_key=True, index=True)
    # content: 답변 내용
    content = Column(Text, nullable=False)
    # create_date: 답변 작성일시
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    
    # question_id: 질문 id (Foreign Key)
    # ForeignKey('question.id')를 사용하여 Question 테이블의 id와 연결
    question_id = Column(Integer, ForeignKey("question.id"), nullable=True) 
    
    # Question 모델과의 관계 정의
    # back_populates="answers"는 Question 모델의 answers 필드와 연결
    question = relationship("Question", back_populates="answers")