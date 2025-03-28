from sqlalchemy.orm import Session
import models, schemas

def create_blog(db: Session, blog: schemas.BlogCreate):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_blogs(db: Session):
    return db.query(models.Blog).all()

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def update_blog(db: Session, blog_id: int, blog_data: schemas.BlogCreate):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog:
        blog.title = blog_data.title
        blog.body = blog_data.body
        db.commit()
        db.refresh(blog)
        return blog
    return None

def delete_blog(db: Session, blog_id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog:
        db.delete(blog)
        db.commit()
        return {"message": "Blog deleted successfully"}
    return {"error": "Blog not found"}
