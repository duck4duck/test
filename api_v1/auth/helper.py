from api_v1.clients.pydantic_schemas import UserSchema
from api_v1.auth import utils as jwt_utils
from . import config
from const import TOKEN_TYPE_FIELD,ACCESS_TOKEN_TYPE,REFRESH_TOKEN_TYPE


def create_jwt(token_type : str,token_data : dict,expire_minutes:int = config.settings.access_token_expire_minutes):
    jwt_payload = {TOKEN_TYPE_FIELD :token_type}
    jwt_payload.update(token_data)
    return jwt_utils.encode_jwt(
    payload=jwt_payload,
    expire_minutes=expire_minutes)



def create_access_token( user : UserSchema):
    jwt_payload = {
        "sub":user.username,
        "username": user.username,
        "email": user.email
    }
    return create_jwt(token_type=ACCESS_TOKEN_TYPE,token_data=jwt_payload,expire_minutes=config.settings.access_token_expire_minutes)




def create_refresh_token(user:UserSchema):
    jwt_payload = {
        "sub":user.username,
        
    }
    return create_jwt(token_type=REFRESH_TOKEN_TYPE,token_data=jwt_payload,expire_minutes=config.settings.refresh_token_expire_days)