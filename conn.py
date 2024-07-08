import sqlalchemy
from sqlalchemy import create_engine
def sql_connection():
    DATABASE_URI = 'sqlite:///books.db'  
    engine = create_engine(DATABASE_URI) 
    conn = engine.connect()
    return conn