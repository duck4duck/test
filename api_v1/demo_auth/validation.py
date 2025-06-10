from fastapi import APIRouter,Depends,Form,HTTPException, Request,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials,OAuth2PasswordBearer
from api_v1.auth import helper
from api_v1.auth import utils as jwt_utils
from jwt import InvalidTokenError

from api_v1.auth import helper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.dbhelper import db_helper
from core.models.schemas import User
from const import COOKIE_REFRESH,COOKIE_ACCESS
from const import TOKEN_TYPE_FIELD,ACCESS_TOKEN_TYPE,REFRESH_TOKEN_TYPE
# oauth_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login/")

def get_token_from_cookie(request:Request,tokenType:str):
    token = request.cookies.get(tokenType)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Missing {tokenType} cookie ")
    
    return token


def get_current_payload(raw_token: str) -> dict:
    try:
        return jwt_utils.decode_jwt(raw_token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")




async def get_current_access_payload(request: Request,) -> dict:
    raw = get_token_from_cookie(request, COOKIE_ACCESS)
    payload = get_current_payload(raw)
    return payload


async def get_current_refresh_user(request: Request,session:AsyncSession = Depends(db_helper.get_smart_session)) -> User:
  return await get_user_from_token(request=request,expected_token_type=REFRESH_TOKEN_TYPE,cookie_name=COOKIE_REFRESH,session=session)
 



async def get_user_from_token(request:Request,expected_token_type:str,cookie_name:str,session:AsyncSession = Depends(db_helper.get_smart_session)):
    raw = get_token_from_cookie(request,cookie_name)
    payload = get_current_payload(raw)
    if(payload.get(TOKEN_TYPE_FIELD) != expected_token_type):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid token type: expected {expected_token_type}")
    stmt = select(User).where(User.username == payload.get("sub"))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")
    
    return user



async def get_current_access_user(request: Request,session:AsyncSession = Depends(db_helper.get_smart_session)) -> User:
    return await get_user_from_token(request=request,expected_token_type=ACCESS_TOKEN_TYPE,cookie_name=COOKIE_ACCESS,session=session)





