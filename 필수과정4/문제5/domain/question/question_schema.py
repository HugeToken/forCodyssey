# domain/question/question_schema.py

from pydantic import BaseModel, Field

class QuestionCreate(BaseModel):
    """
    질문 등록 요청을 위한 Pydantic 스키마
    - subject와 content는 필수 입력이며 빈 값을 허용하지 않습니다.
    """
    subject: str = Field(..., min_length=1, max_length=300, description="질문 제목")
    content: str = Field(..., min_length=1, description="질문 내용")