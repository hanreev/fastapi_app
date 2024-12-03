from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.models.item import Item, ItemIn
from app.models.response import ErrorResponseContent, ResponseContent

db: list[Item] = []

for i in range(1, 11):
    db.append(Item(id=i, name=f'Item {i}', description=f'This is item {i}'))

router = APIRouter(tags=['Items'])


@router.get('/items', response_model=ResponseContent[list[Item]])
async def get_items():
    return ResponseContent(message='Item list', data=db)


@router.post('/items', response_model=ResponseContent[Item], status_code=status.HTTP_201_CREATED)
async def create_item(item_in: ItemIn):
    last_item = sorted(db, key=lambda x: x.id).pop()
    item = Item(id=last_item.id+1, **item_in.model_dump())
    db.append(item)
    return ResponseContent(message='Item created', data=item)


@router.get('/items/{item_id}', response_model=ResponseContent[Item], responses={404: {'model': ErrorResponseContent}})
async def get_item(item_id: int):
    for item in db:
        if item.id == item_id:
            return ResponseContent(message='Item detail', data=item)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponseContent(message='Item not found').model_dump(),
    )


@router.put('/items/{item_id}', response_model=ResponseContent[Item], responses={404: {'model': ErrorResponseContent}})
async def update_item(item_id: int, item_in: ItemIn):
    for item in db:
        if item.id == item_id:
            item.name = item_in.name
            item.description = item_in.description
            return ResponseContent(message='Item detail', data=item)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponseContent(message='Item not found').model_dump(),
    )


@router.delete('/items/{item_id}', response_model=ResponseContent[Item], responses={404: {'model': ErrorResponseContent}})
async def delete_item(item_id: int):
    for item in db:
        if item.id == item_id:
            db.remove(item)
            return ResponseContent(message='Item deleted', data=item)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponseContent(message='Item not found').model_dump(),
    )
