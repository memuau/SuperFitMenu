from fastapi import FastAPI
import os
from pymongo import MongoClient
from routes import ingredient_router, router3
import uvicorn

ATLAS_URI = os.environ['atlas-uri']
DB_NAME = os.environ['db-name']

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(ingredient_router, tags=["ingredients"], prefix="/ingredient")
app.include_router(router3, tags=['test'], prefix='/test')

if __name__ == "__main__":
    uvicorn.run(app, host ="0.0.0.0", port =8000)
