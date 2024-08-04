from typing import List

from pydantic import BaseModel


class GetAttractionsSchema(BaseModel):
    id: int
    title: str


class PostAttractionsSchema(BaseModel):
    title: str
    description: str
