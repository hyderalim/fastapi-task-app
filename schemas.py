from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str

class TaskOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: str
    description: str        