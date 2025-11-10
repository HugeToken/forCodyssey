from pydantic import BaseModel, Field
from typing import Optional

class TodoId(BaseModel):
    '''
    개별 항목 조회를 위한 ID 모델.
    '''
    item_id: int = Field(..., description="조회/수정/삭제할 TODO 항목의 고유 ID")

class TodoItem(BaseModel):
    '''
    새로운 TODO 항목을 생성하거나, 리스트에 저장될 항목의 기본 모델.
    '''
    item: str = Field(..., min_length=1, description="TODO 항목의 내용")

class TodoUpdate(BaseModel):
    '''
    기존 TODO 항목을 수정할 때 사용될 모델.
    Optional을 사용하여 항목 내용(item)의 수정 여부를 선택적으로 처리합니다.
    '''
    item: Optional[str] = Field(None, min_length=1, description="수정할 TODO 항목의 새로운 내용")
