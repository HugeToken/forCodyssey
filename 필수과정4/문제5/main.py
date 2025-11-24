# main.py

from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from database import engine, get_db
from models import Base, Question
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from domain.question import question_router 

app = FastAPI(
    title="Pyboard FastAPI",
    description="SQLAlchemy and FastAPI 게시판 프로젝트"
)

app.include_router(question_router.router, prefix="/api", tags=["question"])


async def create_db_and_tables():
    """비동기 엔진을 사용하여 모델에 정의된 테이블을 생성합니다."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 DB 테이블을 생성합니다 (초기 개발용)."""
    print("FastAPI 애플리케이션 시작")

@app.get("/")
def read_root():
    """기본 루트 경로 엔드포인트"""
    return {"message": "Welcome to Pyboard FastAPI!"}

@app.post("/test/create_question")
async def create_test_question(db: AsyncSession = Depends(get_db)):
    """
    테스트용 질문 데이터를 생성하고 DB에 저장하는 엔드포인트입니다.
    autocommit=False 설정에 따라 commit()이 필수입니다.
    """
    
    new_question = Question(
        subject=f"임시 테스트 질문 - {datetime.now().strftime('%H:%M:%S')}",
        content="이것은 main.py에서 생성된 임시 데이터입니다.",
        create_date=datetime.now()
    )
    
    db.add(new_question)
    
    try:
        await db.commit() 
        await db.refresh(new_question)
        return {"message": "Question created successfully", "id": new_question.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)