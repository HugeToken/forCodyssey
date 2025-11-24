from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Question

# 1. APIRouter 객체 생성
router = APIRouter(
    prefix="/question",
)

# 2. 질문 목록 조회 엔드포인트
@router.get("/list")
async def question_list(db: AsyncSession = Depends(get_db)):
    """
    GET 요청을 처리하여 SQLite의 question 테이블에 있는 
    모든 질문 목록을 비동기적으로 가져옵니다.
    """
    
    # 💡 SQLAlchemy 2.0 스타일로 쿼리 작성: SELECT * FROM question
    # select(Question): Question 모델을 대상으로 하는 SELECT 문을 생성합니다.
    stmt = select(Question).order_by(Question.create_date.desc())
    
    # 💡 DB 실행: 쿼리를 비동기적으로 실행하고 결과를 가져옵니다.
    result = await db.execute(stmt)
    
    # 💡 결과 처리: DB 레코드 객체에서 실제 데이터 객체(Question 모델 인스턴스)를 추출합니다.
    # .scalars()를 사용하여 결과 행 대신 모델 인스턴스를 바로 가져옵니다.
    question_list = result.scalars().all()
    
    # 💡 결과를 JSON 형태로 반환
    return question_list