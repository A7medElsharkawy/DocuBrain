from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings


app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    setting= get_settings()
    app.mongo_conn = AsyncIOMotorClient(setting.MONGO_URI)
    app.db_client = app.mongo_conn[setting.MONGO_DATABASE]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()


app.include_router(base.base_router)
app.include_router(data.data_router)


