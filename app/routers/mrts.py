from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlmodel import Session, select,func
from models import Attraction
from database import engine
from exceptions import *


mrts_router = APIRouter()


@mrts_router.get(
    "/mrts",
    summary="取得捷運站名列表",
    description="取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序",
    responses={
        500: {
            "description": "伺服器內部錯誤",
            "content": {"application/json": {"schema": Error.model_json_schema()}},
        },
    },
)
def get_mrt():
    """取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序"""
    try:
        stmt = (
            select(
                Attraction.mrt,
                func.count(Attraction.name).label("attraction_count"),
            )
            .group_by(Attraction.mrt)
            .order_by(func.count(Attraction.name).desc())
        )
        with Session(engine) as sess:
            mrt_list = sess.exec(stmt).all()
            res = [row[0] for row in mrt_list]
            return {"data":res}
    except Exception as e:
        WebBaseException(
            error=True,
            message=str(e)
        )
