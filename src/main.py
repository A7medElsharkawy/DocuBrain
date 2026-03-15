from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()

async def startup_db_client():
    setting= get_settings()
    app.mongo_conn = AsyncIOMotorClient(setting.MONGO_URI)
    app.db_client = app.mongo_conn[setting.MONGO_DATABASE]

    llm_provider_factory = LLMProviderFactory(setting)
    app.generation_client = llm_provider_factory.create(provider=setting.GERNERATION_BACKEND)
    app.generation_client.set_generation_models(mode_id= setting.GENERATION_MODEL_ID)
    app.emebedding_client = llm_provider_factory.create(provider=setting.EMBEDDING_BACKEND)
    app.generation_client.set_embedding_model(mode_id= setting.EMBEDDDING_MODEL_ID,
                                            embedding_size=setting.EMBEDDDING_MODEL_SIZE)



async def shutdown_db_client():
    app.mongo_conn.close()


app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)


