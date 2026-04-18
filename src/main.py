from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings
from stores import vectoredb
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectoredb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()

async def startup_span():
    setting= get_settings()
    app.mongo_conn = AsyncIOMotorClient(setting.MONGO_URI)
    app.db_client = app.mongo_conn[setting.MONGO_DATABASE]

    llm_provider_factory = LLMProviderFactory(setting)
    vectoredb_provider_factory = VectorDBProviderFactory(setting)

    app.generation_client = llm_provider_factory.create(provider=setting.GERNERATION_BACKEND)
    app.generation_client.set_generation_models(mode_id= setting.GENERATION_MODEL_ID)

    app.emebedding_client = llm_provider_factory.create(provider=setting.EMBEDDING_BACKEND)
    app.emebedding_client.set_embedding_model(mode_id= setting.EMBEDDDING_MODEL_ID,
                                            embedding_size=setting.EMBEDDDING_MODEL_SIZE)
    
    app.vectordb_client = vectoredb_provider_factory.create(
        provider=setting.VECTORE_DB_BACKEND
    )
    app.vectordb_client.connect()


async def shutdown_span():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()


app.router.lifespan.on_startup.append(startup_span)
app.router.lifespan.on_shutdown.append(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)


