from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas, crud


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


@app.post("/blogs/", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.create_blog(db, blog)


@app.get("/blogs/", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
    return crud.get_blogs(db)


# @app.get("/blogs/{blog_id}", response_model=schemas.BlogResponse)
# def get_blog(blog_id: int, db: Session = Depends(get_db)):
#     blog = crud.get_blog(db, blog_id)
#     if blog is None:
#         raise HTTPException(status_code=404, detail="Blog not found")
#     return blog


@app.put("/blogs/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(blog_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return crud.update_blog(db, blog_id, blog)


@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    return crud.delete_blog(db, blog_id)



