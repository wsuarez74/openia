import json
import logging
import llm # type: ignore
from fastapi import FastAPI
from openai import BaseModel
from dotenv import load_dotenv
import os
from typing import Any
import openai

load_dotenv()

logger = logging.getLogger(__name__)

BACKEND_SERVER = os.getenv("SERVER_URL")

app = FastAPI(servers=[{"url": BACKEND_SERVER}])

openai.api_key = os.getenv("org-VJijtoSdzVhF4S9RZkgE00lh")

def get_schema():
    # tu función para obtener el esquema de la base de datos
    pass

def query(sql_query: str):
    # tu función para hacer la consulta a la base de datos
    pass

class PostHumanQueryPayload(BaseModel):
    human_query: str


class PostHumanQueryResponse(BaseModel):
    result: list

@app.post(
    "/human_query",
    name="Human Query",
    operation_id="post_human_query",
    description="Gets a natural language query, internally transforms it to a SQL query, queries the database, and returns the result.",
)

async def human_query(payload: PostHumanQueryPayload):

    # Transforma la pregunta a sentencia SQL
    sql_query = await llm.human_query_to_sql(payload.human_query)

    if not sql_query:
        return {"error": "Falló la generación de la consulta SQL"}
    result_dict = json.loads(sql_query)

    # Hace la consulta a la base de datos
    result = await query(result_dict["sql_query"])

    # Transforma la respuesta SQL a un formato más humano
    answer = await llm.build_answer(result, payload.human_query)
    if not answer:
        return {"error": "Falló la generación de la respuesta"}

    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)