from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Question

router = APIRouter(
    prefix="/question",
)

@router.get("/list")
async def question_list(db: AsyncSession = Depends(get_db)):
    """
    GET 요청을 처리하여 SQLite의 question 테이블에 있는 
    모든 질문 목록을 비동기적으로 가져옵니다.
    """
    
    stmt = select(Question).order_by(Question.create_date.desc())
    
    result = await db.execute(stmt)
    
    question_list = result.scalars().all()
    
    return question_list