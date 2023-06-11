from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import ingredient_router, router3
import uvicorn

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["atlas-uri"])
    app.database = app.mongodb_client[config["db-name"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(ingredient_router, tags=["ingredients"], prefix="/ingredient")
app.include_router(router3, tags=['test'], prefix='/test')

if __name__ == "__main__":
    uvicorn.run(app, host ="0.0.0.0", port =8000)
