# FASTAPI Windows 명령어 목록

# 1. 환경 설정 및 설치

# 작업 디렉토리로 이동 (경로 수정 필요)
cd C:\Codyssey\forCodyssey\필수과정4\문제5

# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화 (PowerShell)
venv\Scripts\Activate.ps1

# 필수 패키지 설치

pip install fastapi "uvicorn[standard]" sqlalchemy "aiosqlite" alembic pydantic pydantic-settings

alembic init alembic

alembic.ini 수정

sqlalchemy.url = driver://user:pass@localhost/dbname 주석처리

alembic/env.py 대체

alembic revision --autogenerate -m "Initial database setup"

alembic upgrade head
# 2. 서버 실행

# FastAPI 서버 실행 (main.py 파일 필요)
uvicorn main:app --reload
