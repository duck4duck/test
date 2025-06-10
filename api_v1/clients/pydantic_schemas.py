from pydantic import BaseModel,ConfigDict, EmailStr



class baseClient(BaseModel):
    __tablename__ = "client_base"

    name : str
    surname : str
    email : EmailStr
    age : int 


class Client(baseClient):
    model_config = ConfigDict(from_attributes=True)
    id: int 




class createClient(baseClient):
    pass


class updateClient(baseClient):
    name: str | None = None
    surname: str | None = None
    age: int | None = None
    email : EmailStr | None = None

class BasicUser(BaseModel):
    username : str
    password : bytes
    email : EmailStr | None = None


class UserSchema(BasicUser):
    model_config = ConfigDict(strict = True)
    username : str
    password : bytes
    email : EmailStr | None = None
