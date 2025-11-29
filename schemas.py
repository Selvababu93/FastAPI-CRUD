from pydantic import BaseModel, Field

class UsersCreateRequest(BaseModel):
    username : str = Field()
    email : str = Field()
    first_name : str = Field()
    last_name : str = Field()
    password : str = Field()
    role : str = Field()
    phone_number : str 

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "username" : "alice",
                "email" : "alice@email.com",
                "first_name" : "Alice",
                "last_name" : "Charlie",
                "password" : "XXXXXX",
                "role" : "admin",
                "phone_number" : "+1 389745620"
            }
        }
    }



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
    
    

class PhoneNumberUpdateRequest(BaseModel):
    old_number : str
    new_number : str
    
class PhoneNumberUpdateResponse(BaseModel):
    new_number : str 