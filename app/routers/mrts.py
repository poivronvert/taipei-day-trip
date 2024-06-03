from typing import List
from typing import List, Optional, Any
from fastapi import APIRouter, Query, Path, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, col, or_, func
from sqlalchemy.orm import joinedload
from models import AttractionBase, Image
import schema
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
                AttractionBase.mrt,
                func.count(AttractionBase.name).label("attraction_count"),
            )
            .group_by(AttractionBase.mrt)
            .order_by(func.count(AttractionBase.name).desc())
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
