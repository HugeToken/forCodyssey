# main.py (수정 완료)

from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from database import engine, get_db
from models import Base, Question
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from domain.question import question_router 
# 💡 [추가] 정적 파일 서빙 및 리디렉션을 위한 임포트
from fastapi.staticfiles import StaticFiles 
from starlette.responses import RedirectResponse, HTMLResponse 

app = FastAPI(
    title="Pyboard FastAPI",
    description="SQLAlchemy and FastAPI 게시판 프로젝트"
)

# 💡 [추가] 정적 파일 서빙 설정
# 'static' 디렉토리에 있는 파일을 '/static' URL 경로를 통해 접근 가능하게 합니다.
# (index.html 파일을 'static' 폴더로 이동해야 함)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(question_router.router, prefix="/api", tags=["question"])


async def create_db_and_tables():
    """비동기 엔진을 사용하여 모델에 정의된 테이블을 생성합니다."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 DB 테이블을 생성합니다 (초기 개발용)."""
    # 💡 [수정] 테이블 생성 함수를 호출하여 DB 테이블이 자동으로 만들어지도록 합니다.
    await create_db_and_tables() 
    print("FastAPI 애플리케이션 시작")

@app.get("/")
def read_root():
    """기본 루트 경로 엔드포인트를 index.html로 리디렉션합니다."""
    # 💡 [수정] 루트 경로로 접속하면 정적 파일 경로로 리디렉션
    return RedirectResponse(url="/static/index.html")

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