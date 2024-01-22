from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import Optional
from database import *

app = FastAPI()
@app.get('/')
def index():
    return {"message": "this is updated"}

# let create the model for creating the post
class CreatePost(BaseModel):
    title : str
    content: str

# model for updating post 
class UpdatePost(BaseModel):
    title : Optional[str] = None
    content: Optional[str] = None
    

# endpoint for creating posts

@app.post('/posts/create/')

def create_post(post_create: CreatePost):
        p_query = "INSERT INTO blog_posts (title, content) VALUES(%s, %s)"
        val = (post_create.title, post_create.content)
        cursor.execute(p_query, val)
        db.commit()
        return {"message": "Post Successfully Created" }




# endpint for for updating post 

@app.put('/posts/{post_id}/')
def update_post(*, post_id: int= Path( description="The id of the post you want to update"), post_title : Optional[str] = None, post_update: UpdatePost):
    
    fetch_update = "SELECT title, content FROM blog_posts WHERE id = %s OR title =  %s"
    cursor.execute(fetch_update, (post_id, post_title))
    existing_post = cursor.fetchone()
     
    if existing_post:
        updated_title = post_update.title if post_update.title is not None else existing_post[0]
        updated_content = post_update.content if post_update.content is not None else existing_post[1]
        
        post_update_query = "UPDATE blog_posts SET title = %s, content = %s WHERE id = %s" 
        updated_values = (updated_title, updated_content, post_id)
        cursor.execute(post_update_query, updated_values)
        db.commit()
        return {"message": "Post updated successfully"} 
    else:
        return{"Error": "post not found"}
 
# endpoint for deleting a post 

@app.delete('/posts')
def delete_post(*, post_id: int= Path(description="The id of the post you want to delete"), post_title: Optional[str] = Query(description="The title of the post you want to delete")):
    d_query = "DELETE FROM blog_posts where id = %s"
    deleted_val = (post_id, post_title)
    cursor.execute(d_query, deleted_val) 
    db.commit()
    return {"message": "Post deleted successfully"}

# Endpoint to view all posts

@app.get('/posts/')
def view_post():
    cursor.execute("SELECT id, title, content FROM blog_posts")
    all_posts = [{"id": id, "title": title, "content": content} for id, title, content in cursor.fetchall()]
    return all_posts
    