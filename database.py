import os
from typing import Any, LiteralString
from sqlalchemy import QueuePool, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

#DB_URL = os.getenv('DB_URL', 'default')
DB_URL = "postgresql+psycopg2://postgresql://postgres:Afsmnz78*@db.zhakdjtqjzpbyotkoikc.supabase.co:5432/postgres"
engine = create_engine(DB_URL, poolclass=QueuePool,pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)

def get_schema() -> LiteralString:
        engine = create_engine(
             "postgresql+psycopg2://postgresql://postgres:Afsmnz78*@db.zhakdjtqjzpbyotkoikc.supabase.co:5432/postgres"
             )
        inspector = inspect(engine)
        table_names = inspector.get_table_names()

        def get_columns_details(table_name: str) -> list[str]:
            columns = inspector.get_columns(table_name)
            return [f"{col['name']} ({col['type']})" for col in columns]
        
        schema_info = []
        for table_name in table_names:
             table_info = [f"Table: {table_name}"]
             table_info.append("Columns:")
             table_info.extend(f"  - {column}" for column in get_columns_details(table_name))
             table_info.append("\n".join(table_info))
     
        engine.dispose()
        return "\n\n".join(schema_info)


async def query(sql_query: str) -> list[dict[str, Any]]:
    print("sql_query", sql_query)
    with Session() as session:
        statement = text(sql_query)
        result = session.execute(statement)
        return [dict(row._mapping) for row in result]
       
def cleanup() -> None:
    engine.dispose()
 