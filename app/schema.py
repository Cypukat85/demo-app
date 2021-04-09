from pydantic import BaseModel, Field
from typing import Optional


class Item(BaseModel):
    item_id: int = Field(..., description='Идентификатор объекта', alias='id')
    value: Optional[str] = Field(
        None,
        description='Значение атрибута объекта',
        example='Булочка с маком'
    )


class ResponseModel(BaseModel):
    result: str = Field(..., description='Текст результата')
