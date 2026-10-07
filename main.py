from fastapi import FastAPI,Body
import sqlite3

app = FastAPI()


conn = sqlite3.connect("test.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS blog (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL, 
        completed BOOLEAN DEFAULT 0
    )
""")
conn.commit()

@app.get("/")
def home():
    return {"message": "Database and Table created successfully!"}

@app.post("/create-blog")
def create_blog(title: str = Body(...),  #Ellipsis ... it state that it is required 
    completed: bool = Body(False),
    creator: str = Body(...)
    ):
    cursor.execute("INSERT INTO blog  (title,completed) VALUES(? ,?) ", (title, int(completed)) )
    conn.commit()
    new_id = cursor.lastrowid
    return {
        "id": new_id,
        "title": title,
        "crated By" :creator,
        "completed": completed,
        "message": "Blog created successfully without Pydantic!"
    }


# PATH PARAMS
@app.delete("/delete-blog/{id}")
def create_blog(id:int):
    cursor.execute("DELETE FROM blog WHERE id = ?",(id,) ) # TUPLE KE ANDAR , LAGAANA PADTA HAI
    conn.commit()
    
    return {
        "message": "Blog Deleted successfully"
    }


# QUERY PARAMS 
@app.delete("/delete-blog") # Removed /{id} from the path
def delete_blog(id: int):   # This automatically becomes a Query Parameter
    cursor.execute("DELETE FROM blog WHERE id = ?", (id,))
    conn.commit()
    
    return {
        "id_deleted": id,
        "message": "Blog Deleted successfully using Query Parameter"
    }


@app.put("/update-blog")
def create_blog(title: str = Body(...),  #Ellipsis ... it state that it is required 
    completed: bool = Body(False),
    creator: str = Body(...),
    id: int = Body(...)
    ):
    cursor.execute(
        "UPDATE blog SET title = ?, completed = ? WHERE id = ?", 
        (title, int(completed), id)
    )
    conn.commit() 


    return {
        "id": id,
        "title": title,
        "crated By" :creator,
        "completed": completed,
        "message": "Blog Update successfully without Pydantic!"
    }


@app.patch("/patchupdate-blog")
def update_blog(
    id: int = Body(...),
    title: str | None = Body(None),
    completed: bool | None = Body(None),
    creator: str | None = Body(None)
):
    fields = []
    values = []

    if title is not None:
        fields.append("title = ?")
        values.append(title)

    if completed is not None:
        fields.append("completed = ?")
        values.append(int(completed))

    # creator is currently not in your blog table,
    # so don't update it in SQL.

    if not fields:
        return {
            "message": "No fields provided for update"
        }

    values.append(id)

    query = f"""
        UPDATE blog
        SET {", ".join(fields)}
        WHERE id = ?
    """

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        return {
            "message": "Blog not found"
        }

    return {
        "id": id,
        "message": "Blog updated successfully"
    }