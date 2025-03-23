from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.connection import engine
from app import app

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Checking database connection...")
    try:
        with engine.connect() as connection:
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed! Error: {str(e)}")
    yield  
    print("Shutting down FastAPI...") 

app.router.lifespan_context = lifespan