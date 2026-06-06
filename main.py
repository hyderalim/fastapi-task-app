from fastapi import FastAPI, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer
from fastapi import Request
from jose import jwt
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
import models, schemas, crud, auth
import uvicorn


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()







security = HTTPBearer()



def get_current_user(credentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")



# Signup
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db, user.email, user.password)

# Login
@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_token({"user_id": db_user.id})
    return {"access_token": token}

@app.post("/tasks")
def create_task(
    task: schemas.TaskCreate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_task(db, task.title, task.description, user_id)

@app.get("/tasks")
def get_tasks(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_tasks(db, user_id)



@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = crud.update_task(db, task_id, task.title, task.description, user_id)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = crud.delete_task(db, task_id, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return deleted