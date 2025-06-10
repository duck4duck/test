from fastapi import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .pydantic_schemas import createClient,updateClient
from sqlalchemy.engine import Result
from core.models.schemas import Client
from typing import Annotated
from fastapi import HTTPException


async def get_clients(session:AsyncSession):
    stmt = select(Client).order_by(Client.id)
    result:Result = await session.execute(stmt)

    clients = result.scalars().all()
    
    return clients



async def get_client(session:AsyncSession,client_id:int):
    stmt = select(Client).where(Client.id == client_id)
    result:Result = await session.execute(stmt)
    client = result.scalars().first()
    return client 

async def add_clients(session:AsyncSession,new_client:createClient ):
    
    client = Client(**new_client.model_dump())
    session.add(client)
    await session.commit()

    return client

async def full_update_clients(session:AsyncSession,upd_client:updateClient,client_id:int):
    my_client = await get_client(session=session,client_id=client_id)

    if not my_client:
        raise HTTPException(status_code=404,detail="user not found")
    
    updated_info = upd_client.model_dump()

    for key,value in updated_info.items():
        setattr(my_client,key,value)

    await session.commit()
    return my_client



async def update_clients(session:AsyncSession,upd_client : updateClient,client_id:Annotated[int,Path] ):
    my_client = await get_client(session=session,client_id=client_id)
    if not my_client:
        raise HTTPException(status_code=404,detail="user not found")

    my_new_client = upd_client.model_dump(exclude_unset=True)
    for key,value in my_new_client.items():
        setattr(my_client,key,value)
    await session.commit()
    return my_client


async def delete_client(session:AsyncSession,client_id:int ):
     del_client = await get_client(session=session,client_id=client_id)
     await session.delete(del_client)
     await session.commit()