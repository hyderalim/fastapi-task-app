from sqlalchemy.orm import Session
import models, auth

def create_user(db: Session, email: str, password: str):
    user = models.User(
        email=email,
        password=auth.hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not auth.verify_password(password, user.password):
        return None
    return user

def create_task(db, title: str, description: str, user_id: int):
    task = models.Task(
        title=title,
        description=description,
        owner_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()


def update_task(db, task_id: int, title: str, description: str, user_id: int):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()

    if not task:
        return None

    task.title = title
    task.description = description
    db.commit()
    db.refresh(task)
    return task


def delete_task(db, task_id: int, user_id: int):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()

    if not task:
        return None

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}