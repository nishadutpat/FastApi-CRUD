from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from database import engine, get_db
import models, schemas, crud
from auth import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/blogs/", response_model=schemas.BlogResponse)
def create_blog(
    blog: schemas.BlogCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  
):
    return crud.create_blog(db, blog)


@app.get("/blogs/", response_model=list[schemas.BlogResponse])
def get_blogs(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  
):
    return crud.get_blogs(db)


@app.put("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(
    blog_id: int, 
    blog: schemas.BlogCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user) 
):
    return crud.update_blog(db, blog_id, blog)


@app.delete("/blogs/{blog_id}")
def delete_blog(
    blog_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)  
):
    return crud.delete_blog(db, blog_id)


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['full_name']}, you have access!"}
