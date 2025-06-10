import jwt
import bcrypt
from datetime import timedelta,datetime
from core.config import settings
from datetime import datetime, timedelta




def encode_jwt(
        payload:dict ,
        private_key : str = settings.auth_jwt.private_key_path.read_text(),
        algorithm : str =  settings.auth_jwt.algorithm,
        expire_minutes:int = settings.access_token_expire_minutes
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    exp = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp = exp,iat = now)
    encoded = jwt.encode(to_encode,private_key,algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token,public_key,algorithms=[algorithm])
    return decoded 


def hash_password(password : str):
    salt = bcrypt.gensalt()
    pwd_bytes : bytes=password.encode()
    return bcrypt.hashpw(pwd_bytes,salt)






def validate_password(password:str,hashed_password:bytes):
    return bcrypt.checkpw(password.encode(),hashed_password)
    