
from fastapi import FastAPI
import uvicorn

from core.models.dbhelper import db_helper
from core.models.schemas import Base
from api_v1 import router as client_router
from api_v1 import s3_client

from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app:FastAPI):
    async with db_helper.engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    await s3_client.create_bucket()
    
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router=client_router)


@app.get("/")
def hello():
    return {"message":"Hello guys!"}








if __name__ =='__main__':
    uvicorn.run("main:app",reload = True)