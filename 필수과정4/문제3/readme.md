============================================================
FASTAPI TO-DO 시스템 Windows 명령어 목록
============================================================

# 1. 환경 설정 및 설치

# 작업 디렉토리로 이동 (경로 수정 필요)
cd C:\Codyssey\forCodyssey\필수과정4\문제3

# 가상 환경 생성
python -m venv .venv

# 가상 환경 활성화 (PowerShell)
.venv\Scripts\Activate.ps1

# 필수 패키지 설치
pip install fastapi "uvicorn[standard]"

# 2. 서버 실행

# FastAPI 서버 실행 (todo.py 파일 필요)
uvicorn todo:app --reload

# 3. API 테스트 (PowerShell 기준)

# TODO 리스트 조회 (GET)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/todos" -Method Get

# 항목 추가 (POST)
$body = '{"item": "hihi"}'
$body = '{"item": ""}'
Invoke-RestMethod -Uri "http://127.0.0.1:8000/todos" -Method Post -ContentType "application/json" -Body $body