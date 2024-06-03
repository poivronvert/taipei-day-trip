from typing import List, Optional, Any
from fastapi import APIRouter, Query, Path, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, col, or_
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from models import AttractionBase, Image
import schema
from database import engine
from exceptions import *

attraction_router = APIRouter()


@attraction_router.get(
    "/attractions",
    summary="取得景點資料列表",
    description="取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字、或捷運站名稱篩選",
    responses={
        500: {
            "description": "可能沒找到資料喔",
            "content": {"application/json": {"schema": Error.model_json_schema()}},
        },
    },
)
async def get_attraction(
    page: int = Query(0, description="要取得的分頁，每頁 12 筆資料", ge=0),
    keyword: Optional[str] = Query(
        None,
        description="用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選",
    ),
) -> schema.AttractionOut | AttractionInternalErrorSchema | Error:
    page_size: int = 12
    with Session(engine) as session:
        query = select(AttractionBase).options(
            joinedload(AttractionBase.images).load_only(Image.url)
        )
        if keyword:
            query = query.where(
                or_(
                    AttractionBase.mrt == keyword, AttractionBase.name.contains(keyword)
                )
            )
        cnt_stmt = select(func.count()).select_from(query.subquery())
        cnt = session.exec(cnt_stmt).first()
        attractions = session.exec(query.offset(page * page_size).limit(page_size)).unique().all()
        if not attractions:
            raise AttractionInternalError(message="沒有資料")

        res = []
        for a in attractions:
            _attraction = a.model_dump()
            _attraction["images"] = [_.url for _ in a.images]
            res.append(_attraction)

        nextpage = page + 1
        if (cnt - ((page+1) * page_size)) <=12:
            nextpage = None # meaning that is last page. 

        return {"nextPage": nextpage, "data": res}


@attraction_router.get(
    "/attraction/{attractionId}",
    summary="根據景點編號取得景點資料",
    responses={
        400: {
            "description": "景點編號不正確",
            "content": {"application/json": {"schema": Error.model_json_schema()}},
        },
    },
)
def get_attraction_id(
    attractionId: int = Path(description="景點編號"),
) -> schema.AttractionIdOut:
    with Session(engine) as session:
        attraction = session.exec(
            select(AttractionBase).filter_by(id=attractionId)
        ).first()
        if not attraction:
            raise AttractionInternalError(status_code=400, message="沒有資料")
        data = attraction.model_dump()
        data["images"] = [i.url for i in attraction.images]
        return {"data": data}
