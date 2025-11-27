from fastapi import FastAPI
from database import engine
import models
from routes import auth, todos, admin, users


app = FastAPI(
    title="Todo App",
    version="1.0.0"
)

models.Base.metadata.create_all(engine)

app.include_router(auth.router, prefix='/auth', tags=['Auth'])
app.include_router(todos.router, prefix='/todos', tags=['Todos'])
app.include_router(admin.router, prefix='/admin', tags=['Admin'])
app.include_router(users.router, prefix='/user', tags=['User'])

@app.get("/")
async def root():
    return "TODO App Demo"


