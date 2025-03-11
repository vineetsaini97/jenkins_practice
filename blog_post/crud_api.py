from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor



app=FastAPI()


db_name="blog_post"
db_usr="postgres"
db_passwd="apple"
db_host="db"
db_port="5432"

conn=psycopg2.connect(
    database=db_name,
    user=db_usr,
    password=db_passwd,
    host=db_host,
    port=db_port
)

class Roles(BaseModel):
    name: str
    description: str

select_query="SELECT * FROM roles WHERE id=%s"


@app.post("/roles")
def add_role(role:Roles):
    cursor = conn.cursor()
    select_query="SELECT * FROM roles WHERE name=%s"
    cursor.execute(select_query,(role.name,))
    name=cursor.fetchone()
    if name:
        cursor.close()
        return {"Role already exists" : f"{role.name} already exists, please try with a different name."}
    insert_query="INSERT INTO roles(name,description) VALUES(%s,%s)"
    cursor.execute(insert_query,(role.name,role.description))
    conn.commit()
    cursor.close()
    return {"Data Added successfully" : role}
    


@app.get("/all-roles")
def get_roles():
    cursor=conn.cursor(cursor_factory=RealDictCursor) 
    select_query="SELECT * FROM roles ORDER BY id "
    cursor.execute(select_query)
    roles=cursor.fetchall()
    cursor.close()
    if roles:
        return roles
    else:
        return {"Message": "There are no roles added in the database."}
    

@app.get("/roles/{id}")
def get_role(id:int):
    cursor=conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(select_query,(id,))
    role:Roles=cursor.fetchone()
    cursor.close()
    if role:
        return role
    else:
        return {"Message" : f"There is no such role exists with this id : {id}."}
   

    

@app.put("/roles/{id}")
def update_role(id:int,role:Roles):
    cursor=conn.cursor()
    select_query="SELECT name FROM roles WHERE id=%s"
    cursor.execute(select_query,(id,))
    data=cursor.fetchone()
    # function to update data
    def update_data():
            update_query="UPDATE roles SET name=%s , description=%s  where id=%s"
            cursor.execute(update_query,(role.name,role.description,id))
            conn.commit()
            cursor.close()
    
    if data:
        if data==role.name:
            update_data()
            return {"Message" : "data updated successfully."}
        select_query="SELECT * FROM roles WHERE name=%s and id!=%s"
        cursor.execute(select_query,(role.name,id))
        data=cursor.fetchone()
        if data:
            return {"Message" :" Having the same role name that already exists in database."}
        update_data()
        return {"Message" : "data updated successfully."}
    return {"Message": f"no data exists with this id,{id}"}

# @app.put("/roles/{id}")
# def update_role(id:int,role:Roles):
#     cursor=conn.cursor()
#     select_query="SELECT name FROM roles WHERE id=%s"
#     cursor.execute(select_query,(id,))
#     data=cursor.fetchone()
#     if data:
#         select_query="SELECT * FROM roles WHERE name=%s and id!=%s"
#         cursor.execute(select_query,(role.name,id))
#         data=cursor.fetchone()
#         if data:
#             return {"Message" :" Having the same role name that already exists in database."}
#         update_query="UPDATE roles SET name=%s , description=%s  where id=%s"
#         cursor.execute(update_query,(role.name,role.description,id))
#         conn.commit()
#         cursor.close()
#         return {"Message" : "data updated successfully."}
#     return {"Message": f"no data exists with this id,{id}"}


@app.delete("/roles/{id}")
def delete_role(id:int):
    cursor=conn.cursor()
    cursor.execute(select_query,(id,))
    role=cursor.fetchone()
    if role:
        delete_query="DELETE FROM roles WHERE id=%s"
        cursor.execute(delete_query,(id,))
        conn.commit()
        cursor.close()
        return {"Data deleted successfully" : role}
    else:
        return {"Message:" : f"There are no roles added in the database with this id {id}"}
    

    