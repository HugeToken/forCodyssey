from fastapi import FastAPI, APIRouter, HTTPException
from typing import Dict, List

app = FastAPI(title='Simple To-Do API')

todo_list: List[Dict[str, str]] = []

router = APIRouter(
    prefix='/todos',
    tags=['To-Do Items']
)

@router.post('/')
def add_todo(todo_item: Dict[str, str]):
    '''
    새로운 TODO 항목을 리스트에 추가합니다.
    - 입력: Dict[str, str] 타입 (예: {'item': '숙제하기'})
    - 입력 항목이 비어 있으면 400 경고를 반환합니다.
    '''
    if not todo_item or 'item' not in todo_item or not todo_item['item'].strip():
        raise HTTPException(
            status_code=400,
            detail={'message': 'TODO 항목은 비어 있거나 \'item\' 키가 누락될 수 없습니다.'}
        )

    todo_list.append(todo_item)
    return {'message': 'TODO 항목이 성공적으로 추가되었습니다.', 'item': todo_item['item']}

@router.get('/')
def retrieve_todo():
    '''
    현재 저장된 전체 TODO 리스트를 반환합니다.
    - 출력: Dict[str, List] 타입
    '''
    return {'todo_list': todo_list, 'count': len(todo_list)}

app.include_router(router)

@app.get('/', tags=['status'])
def root():
    return {'message': 'FastAPI To-Do System is running!', 'docs_url': '/docs'}