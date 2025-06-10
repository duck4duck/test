from fastapi import Depends,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from core.models.dbhelper import db_helper
from .pydantic_schemas import createClient,updateClient,Client


router = APIRouter(tags=["clients"])


@router.get("/")
async def check_clients(session:AsyncSession = Depends(db_helper.get_smart_session)):
    
    return await crud.get_clients(session=session)


@router.post("/")
async def new_clients(new_client : createClient,session : AsyncSession = Depends(db_helper.get_smart_session)):
    
    return await crud.add_clients(session=session,new_client=new_client)


@router.get("/{client_id}/")
async def check_one_client(client_id:int,session:AsyncSession = Depends(db_helper.get_smart_session)):
    return await crud.get_client(session=session,client_id=client_id)


@router.patch("/{client_id}/")
async def update_Client(upd_client:updateClient ,client_id:int,session:AsyncSession = Depends(db_helper.get_smart_session)):
    return await crud.update_clients(session = session,upd_client=upd_client,client_id=client_id,)



@router.put("/{client_id}/")
async def full_update_clients(upd_client:updateClient,client_id:int,session:AsyncSession = Depends(db_helper.get_smart_session)):
    return await crud.full_update_clients(session=session,upd_client=upd_client,client_id=client_id)

@router.delete("/{client_id}/")
async def delete_client(client_id:int,session:AsyncSession = Depends(db_helper.get_smart_session)):
    return await crud.delete_client(session=session,client_id=client_id)