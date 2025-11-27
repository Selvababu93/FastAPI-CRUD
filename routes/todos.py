from fastapi import APIRouter, HTTPException, status, Depends, Path
from database import db_dependency
from database import db_dependency
from security import user_dependency
from models import Todos
from typing import Annotated
from schemas import TodosCreateRequest, TodosCreateResponse


router = APIRouter()


@router.get("/")
async def read_all(db: db_dependency, user: user_dependency):
    try:
        todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        if not todo_model:
            return "No Todos yet"
        
        return todo_model
    except Exception as e:
        print(f"DB Error {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    


@router.post("/", response_model=TodosCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, user: user_dependency, request: TodosCreateRequest):
    try:
        todo_model = Todos(
            title = request.title,
            description = request.description,
            priority = request.priority,
            owner_id = user.get("id")
        )
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
        return todo_model
    except Exception as e:
        print(f"DB Error {e}")
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail="Internal server error")
    

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, user: user_dependency, todo_id : int = Path(gt=0)):
    try:
        todo_model = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.get('id')).first()
        if not todo_model:
            return "Todo Not Found"
        return todo_model
    
    except Exception as e:
        print(f"DB Error {e}")
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail="Internal server error")
    


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(db: db_dependency, user: user_dependency, todo_id : int = Path(gt=0)):
    try:
        todo_model = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.get('id')).first()
        if not todo_model:
            return "Todo Not Found"
        
        db.delete(todo_model)
        db.commit()
        return 
    except Exception as e:
        print(f"DB Error {e}")
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail="Internal server error")
