from fastapi import Request, Depends, APIRouter, Body, Path, Query, Response
from asyncpgsa.connection import SAConnection
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from typing import List, Optional, Union
from app.model import items
from app.schema import Item, ResponseModel
from app.dependencies import get_postgresql_connection

router = APIRouter()


@router.get(
    '/item/',
    name='Получить все элементы',
    response_model=Union[List[Item], ResponseModel]
)
async def get_items(
        request: Request,
        response: Response,
        db: SAConnection = Depends(get_postgresql_connection)
):
    """Getting all items list"""
    if db is None:
        response.status_code = 503
        return ResponseModel(result='Service unavailable')
    q = items.select()
    result = await db.fetch(query=q)
    items_list = [Item(**item) for item in result]
    return items_list


@router.post(
    '/item/',
    name='Создать новый элемент',
    response_model=ResponseModel,
    status_code=201
)
async def create_item(
        request: Request,
        response: Response,
        value: str = Body(
            ...,
            desccription='Значение для нового элемента',
            example='Булочка с маком',
            embed=True
        ),
        db: SAConnection = Depends(get_postgresql_connection)
):
    """Create new item"""
    if db is None:
        response.status_code = 503
        return ResponseModel(result='Service unavailable')
    q = insert(items).values(value=value)
    created_item_id = await db.fetchval(q)
    return ResponseModel(result=created_item_id)


@router.get(
    '/item/{item_id}',
    name='Получение одного элемента',
    response_model=Item
)
async def get_item(
        request: Request,
        response: Response,
        item_id: int,
        db: SAConnection = Depends(get_postgresql_connection)
):
    """Get item by id"""
    if db is None:
        response.status_code = 503
        return ResponseModel(result='Service unavailable')
    q = items.select().where(items.c.id == item_id)
    item = await db.fetchrow(query=q)
    print(item)
    if item is not None:
        return Item(**item)
    else:
        response.status_code = 404


@router.put(
    '/item/{item_id}',
    name='Обновить элемент',
    response_model=ResponseModel
)
async def update_item(
        request: Request,
        response: Response,
        item_id: int = Path(..., description='Item ID '),
        value: str = Body(
            None,
            embed=True,
            description='Новое значение элемента', example='Торт "Наполеон"'),
        db: SAConnection = Depends(get_postgresql_connection)
):
    """Update item"""
    if db is None:
        response.status_code = 503
        return ResponseModel(result='Service unavailable')
    q = items.update().values(value=value).where(items.c.id == item_id)
    result = await db.fetch(query=q)
    return ResponseModel(result='ok')


@router.delete(
    '/item/{item_id}',
    name='Удалить элемент',
    response_model=ResponseModel
)
async def delete_item(
        request: Request,
        response: Response,
        item_id: int = Path(..., description='Item ID '),
        db: SAConnection = Depends(get_postgresql_connection)
):
    """Delete item"""
    if db is None:
        response.status_code = 503
        return ResponseModel(result='Service unavailable')
    q = items.delete().where(items.c.id == item_id)
    result = await db.fetch(query=q)
    return ResponseModel(result='ok')
