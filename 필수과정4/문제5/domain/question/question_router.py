# domain/question/question_router.py

from fastapi import APIRouter, Depends, HTTPException, status
# 💡 [해결] BaseModel, ConfigDict, List, select, QuestionModel 임포트 누락 수정
from pydantic import BaseModel, ConfigDict
from typing import List
from sqlalchemy.future import select 
# QuestionModel은 models.py의 Question 모델을 별칭으로 사용합니다.
from models import Question as QuestionModel, Question # Question은 등록 시 사용
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from datetime import datetime
from domain.question.question_schema import QuestionCreate 


# 💡 [정리] 라우터 객체를 한 번만 정의합니다.
router = APIRouter(
    prefix="/question",
    tags=["question"] # 태그를 추가하여 OpenAPI 문서에서 구분
)


# --- 1. 응답용 Pydantic 스키마 정의 ---
# 💡 [수정] Pydantic을 import 했으므로 이제 정상적으로 작동합니다.
class QuestionSchema(BaseModel):
    """
    Pydantic Question 스키마 (데이터 응답 구조 정의)
    """
    id: int
    subject: str
    content: str
    create_date: datetime

    # ORM 객체를 Pydantic으로 변환할 수 있도록 설정
    model_config = ConfigDict(from_attributes=True) 
# ----------------------------------------


@router.get("/list", response_model=List[QuestionSchema])
async def question_list(db: AsyncSession = Depends(get_db)):
    """
    GET 요청을 처리하여 SQLite의 question 테이블에 있는 
    모든 질문 목록을 비동기적으로 가져옵니다.
    """
    
    # QuestionModel 대신 models에서 Question을 직접 임포트했습니다.
    stmt = select(QuestionModel).order_by(QuestionModel.create_date.desc())
    
    result = await db.execute(stmt)
    
    question_list = result.scalars().all()
    
    return question_list


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def question_create(
    question_create: QuestionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    새로운 질문을 등록하는 엔드포인트입니다.
    ORM을 사용하여 DB에 데이터를 삽입하고, 트랜잭션을 커밋합니다.
    """
    
    new_question = Question( # 💡 models에서 임포트한 Question ORM 모델 사용
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now()
    )

    db.add(new_question)
    
    try:
        await db.commit() 
        
    except Exception as e:
        await db.rollback()
        # 실제 데이터베이스 오류를 로깅하거나 상세히 알리는 것이 좋습니다.
        raise HTTPException(status_code=500, detail=f"Database insertion error: {str(e)}")

    return