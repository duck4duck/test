
from api_v1.clients.pydantic_schemas import UserSchema
from api_v1.auth import utils as jwt_utils
from api_v1.auth import helper

from fastapi import APIRouter,Depends,Form,HTTPException,status,Response,Request
from pydantic import BaseModel, EmailStr
from api_v1.demo_auth.validation import get_current_access_user,get_current_refresh_user,get_current_access_payload,get_current_payload
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.dbhelper import db_helper
from core.models.schemas import User
from sqlalchemy import select
from core import config
from const import COOKIE_ACCESS,COOKIE_REFRESH,TOKEN_TYPE_FIELD,REFRESH_TOKEN_TYPE




# http_bearer = HTTPBearer(auto_error=False)
# oauth_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login/")
router = APIRouter(prefix="/jwt",tags=["JWT"])
# router = APIRouter(prefix="/jwt",tags=["JWT"],dependencies=[Depends(http_bearer)])


class TokenInfo(BaseModel):
    access_token : str
    refresh_token: str | None = None
    token_type : str = "Bearer"
    


async def validate_auth_user(username : str = Form(),password : str = Form(),session : AsyncSession = Depends(db_helper.get_smart_session)):
    unauthed_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid username or password")
    
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise unauthed_exc
    


    if not jwt_utils.validate_password(password=password,hashed_password= (user.password).encode("utf-8")):
        raise unauthed_exc
    
    return user


async def validate_reg(username : str = Form(),password : str = Form(),email:EmailStr = Form(),session : AsyncSession = Depends(db_helper.get_smart_session)):
    
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(detail="Пользователь уже существует")
   
    hashed_password = jwt_utils.hash_password(password).decode('utf-8')
    newUser = User(username=username, password=hashed_password, email=email)
    session.add(newUser)
    await session.commit()
    
    return {"message":"Пользователь успешно зарегестрирован"}


@router.post("/login/",response_model=TokenInfo)
def auth_user_issue_jwt(
    response:Response,user : UserSchema = Depends(validate_auth_user)):
    access_token = helper.create_access_token(user)
    refresh_token = helper.create_refresh_token(user)

    response.set_cookie(key=COOKIE_ACCESS,value=access_token,httponly=False,secure=False,samesite="lax",max_age=config.settings.access_token_expire_minutes)
    response.set_cookie(key=COOKIE_REFRESH,value=refresh_token,httponly=False,secure=False,samesite="lax",max_age=config.settings.refresh_token_expire_days)
    return TokenInfo(access_token=access_token,
                     refresh_token = refresh_token)

    
@router.post("/refresh/",response_model=TokenInfo,response_model_exclude_none=True)
def auth_refresh_jwt(response:Response,user:UserSchema = Depends(get_current_refresh_user)):
    access_token = helper.create_access_token(user)
    refresh_token = helper.create_refresh_token(user)

    response.set_cookie(key=COOKIE_ACCESS,value=access_token,httponly=False,secure=False,samesite="lax",max_age=config.settings.access_token_expire_minutes)
    return TokenInfo(access_token=access_token,refresh_token=refresh_token)


@router.post("/registrer/")
def registration(user:UserSchema = Depends(validate_reg)):
    return {
        "message":"Пользователь успешно зарегистрирован"
    }


def get_current_active_auth_user(user:UserSchema = Depends(get_current_access_user)):
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user inactive")
    

@router.get("/users/me")
def get_user_self_info(user:UserSchema = Depends(get_current_access_user),payload:dict = Depends(get_current_access_payload)):
    print(user)
    iat = payload.get("iat")
    return {
        "username":user.username,
        "email":user.email,
        "logged in":iat
    }




