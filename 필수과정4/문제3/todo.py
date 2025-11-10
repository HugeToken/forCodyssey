from fastapi import FastAPI, APIRouter, HTTPException, Path, status
from typing import List, Dict, Any
from model import TodoItem, TodoUpdate

app = FastAPI(title='Advanced To-Do API')

todo_counter = 0

todo_list: List[Dict[str, Any]] = []

router = APIRouter(
    prefix='/todos',
    tags=['To-Do Items']
)

@router.post('/', response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def add_todo(item: TodoItem):
    global todo_counter
    todo_counter += 1
    
    new_todo = {'id': todo_counter, 'item': item.item}
    todo_list.append(new_todo)
    
    return {'message': 'TODO 항목이 성공적으로 추가되었습니다.', 'id': new_todo['id']}


@router.get('/', response_model=Dict[str, Any])
def retrieve_todo():
    '''
    현재 저장된 전체 TODO 리스트를 반환합니다.
    '''
    return {'todo_list': todo_list, 'count': len(todo_list)}


@router.get('/{item_id}', response_model=Dict[str, Any])
def get_single_todo(item_id: int = Path(..., description="조회할 TODO 항목의 고유 ID", gt=0)):
    '''
    ID를 이용해 특정 TODO 항목을 조회합니다.
    '''
    for todo in todo_list:
        if todo['id'] == item_id:
            return todo
            
    raise HTTPException(
        status_code=404, 
        detail={'message': f'{item_id}번 ID를 가진 TODO 항목을 찾을 수 없습니다.'}
    )


@router.put('/{item_id}', response_model=Dict[str, Any])
def update_todo(
    item_id: int = Path(..., description="수정할 TODO 항목의 고유 ID", gt=0),
    new_data: TodoUpdate = None
):
    '''
    ID를 이용해 특정 TODO 항목의 내용을 수정합니다.
    '''
    for todo in todo_list:
        if todo['id'] == item_id:
            if new_data.item is not None:
                todo['item'] = new_data.item
                return {'message': f'{item_id}번 TODO 항목이 성공적으로 수정되었습니다.', 'item': todo['item']}
            else:
                return {'message': f'{item_id}번 TODO 항목의 내용이 변경되지 않았습니다.'}
    
    raise HTTPException(
        status_code=404, 
        detail={'message': f'{item_id}번 ID를 가진 TODO 항목을 찾을 수 없어 수정할 수 없습니다.'}
    )


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_single_todo(item_id: int = Path(..., description="삭제할 TODO 항목의 고유 ID", gt=0)):
    '''
    ID를 이용해 특정 TODO 항목을 삭제합니다.
    '''
    global todo_list
    
    initial_length = len(todo_list)
    
    todo_list = [todo for todo in todo_list if todo['id'] != item_id]
    
    if len(todo_list) == initial_length:
        raise HTTPException(
            status_code=404, 
            detail={'message': f'{item_id}번 ID를 가진 TODO 항목을 찾을 수 없어 삭제할 수 없습니다.'}
        )
        
    return 


app.include_router(router)

@app.get('/', tags=['status'])
def root():
    return {'message': 'FastAPI To-Do System is running!', 'docs_url': '/docs'}