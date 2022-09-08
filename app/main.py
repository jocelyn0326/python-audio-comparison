import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import get_mongo_config
from app.db import db
from app.routers import data

app = FastAPI(title="Syncopate Comparison Server")

app.include_router(data.router, prefix="/api/data")


@app.on_event("startup")
async def startup():
    mongo_config = get_mongo_config()
    await db.connect_to_database(path=mongo_config.db_path)


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Invalid request schema"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
