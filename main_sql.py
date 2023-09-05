from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import List, Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# APP initialization
app = FastAPI()

# DB initialization:
while True:
    try:
        # DB  connection and Custor for SQL operation
        conn = psycopg2.connect(host='localhost', database='Idea_win',
                                user='postgres', password='Welcome123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()

        print("DB connection successfull")
        break

    except Exception as error:
        print("DB connection failed")
        print("Error", error)
        time.sleep(10)

# Schema for the API using pydantic model


class Idea(BaseModel):
    shortName: str
    define: str
    objective: str
    businessValue: Optional[str] = None
    contacts: Optional[str] = None
    status: str
    createdby: str

# API requstes for out ideation application


@app.get("/")
async def root():
    return {"message": "Hello API"}


@app.get("/ideas")
async def get_ideas():
    cursor.execute("""SELECT * FROM ideas """)
    ideas = cursor.fetchall()
    # print(ideas)
    return {"ideas": ideas}


@app.post("/ideas", status_code=status.HTTP_201_CREATED)
async def create_idea(Idea: Idea):
    cursor.execute(
        """ INSERT INTO ideas (shortname,define,objective,businessvalue,contact,status,createdby) VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING * """, (Idea.shortName, Idea.define, Idea.objective, Idea.businessValue, Idea.contacts, Idea.status, Idea.createdby))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get("/ideas/latest")
async def get_latest_idea():
    cursor.execute(""" SELECT * FROM ideas ORDER BY createdat DESC """)
    latest = cursor.fetchone()
    return {"details": latest}


@app.get("/ideas/{id}")
async def get_idea(id: int, response: Response):

    cursor.execute(f"""SELECT * FROM ideas WHERE id={id} """)
    idea = cursor.fetchone()

    if not idea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"idea id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"the {id} is not available in the database"}

    return {"message": idea}


@app.delete("/ideas/{id}")
async def delete_ideas(id: int, response: Response):
    cursor.execute(f"""DELETE FROM ideas WHERE id = {id} RETURNING *""")
    deleted = cursor.fetchone()
    conn.commit()
    if deleted != None:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                            detail=f"Idea ID {id} is deleted from the list")
    elif deleted == None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/ideas/{id}")
async def update_ideas(id: int, response: Response, idea: Idea):
    cursor.execute("""UPDATE ideas SET shortname = %s, define = %s,objective = %s,businessvalue = %s,contact = %s,status = %s,createdby = %s  WHERE id = %s RETURNING *""",
                   (idea.shortName, idea.define, idea.objective, idea.businessValue, idea.contacts, idea.status, idea.createdby, id))
    updated = cursor.fetchone()
    conn.commit()
    if updated != None:
        return {"message": updated}
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
