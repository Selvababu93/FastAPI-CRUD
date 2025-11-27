from pydantic import BaseModel, Field

class UsersCreateRequest(BaseModel):
    username : str = Field()
    email : str = Field()
    first_name : str = Field()
    last_name : str = Field()
    password : str = Field()
    role : str = Field()




class UserCreateResponse(BaseModel):
    id : int
    username : str
    email : str



   
class TodosCreateRequest(BaseModel):
    title : str = Field()
    description : str = Field()
    priority : int = Field(gt=0, lt=6)
    
    
    
class TodosCreateResponse(BaseModel):
    title : str 
    description : str 
    priority : int 
    
    
class Token(BaseModel):
    access_token : str
    token_type : str



class PasswordChangeRequest(BaseModel):
    password : str
    new_password : str