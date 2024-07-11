import sys
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

from routers.user import user_router
from routers.attraction import attraction_router
from routers.mrts import mrts_router
from routers.booking import booking_router
from routers.order import order_router
from exceptions import *



app=FastAPI()

app.include_router(user_router, prefix="/api", tags=["User"])
app.include_router(attraction_router, prefix="/api", tags=["Attraction"])
app.include_router(mrts_router, prefix="/api", tags=["MRT Station"])
app.include_router(booking_router, prefix="/api", tags=["Booking"])
app.include_router(order_router, prefix="/api", tags=["Order"])

app.add_exception_handler(WebBaseException, general_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)


app.mount('/static',StaticFiles(directory='static'),name='static')

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")


if __name__== "__main__":
	try:
		uvicorn.run("main:app", reload=True, host="127.0.0.1")
	except Exception as e:
		sys.exit(1)