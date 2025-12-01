from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
# 💡 [추가] Pydantic을 사용하기 위해 임포트
from pydantic import BaseModel, ConfigDict 
from datetime import datetime

from database import get_db
from models import Question as QuestionModel

class QuestionSchema(BaseModel):
    """
    Pydantic Question 스키마 (데이터 응답 구조 정의)
    """
    id: int
    subject: str
    content: str
    create_date: datetime

    model_config = ConfigDict(from_attributes=True) 
router = APIRouter(
    prefix="/question",
)

@router.get("/list", response_model=List[QuestionSchema])
async def question_list(db: AsyncSession = Depends(get_db)):
    """
    GET 요청을 처리하여 SQLite의 question 테이블에 있는 
    모든 질문 목록을 비동기적으로 가져옵니다.
    """
    
    stmt = select(QuestionModel).order_by(QuestionModel.create_date.desc())
    
    result = await db.execute(stmt)
    
    question_list = result.scalars().all()
    
    return question_list