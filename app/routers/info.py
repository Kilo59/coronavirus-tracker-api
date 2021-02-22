"""app.routers.info"""
from fastapi import APIRouter
from pydantic import BaseModel

API_INFO = APIRouter()


class Info(BaseModel):
    pass
