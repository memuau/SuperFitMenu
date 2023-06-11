from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Book, BookUpdate, Ingredient

router = APIRouter()
ingredient_router = APIRouter()

router3 = APIRouter()

@ingredient_router.get("/", response_description="List all ingredients", response_model=List[Ingredient])
def list_ingredients(request: Request):
    ingredients = list(request.app.database["ingredients"].find(limit=100))
    return ingredients

@router3.get("/test")
def test(request: Request):
    return {"Hello": "Maciej"}

@ingredient_router.post("/create", response_description="Create a new ingredient", status_code=status.HTTP_201_CREATED, response_model=Ingredient)
def create_ingredient(request: Request, ingredient: Ingredient = Body(...)):
    ingredient = jsonable_encoder(ingredient)
    new_ingredient = request.app.database["ingredients"].insert_one(ingredient)
    created_ingredient = request.app.database["ingredients"].find_one(
        {"_id": new_ingredient.inserted_id}
    )

    return created_ingredient

@ingredient_router.get("/{name}", response_description="Get ingredient by name", response_model=List[Ingredient])
def get_ingredients_by_name(name: str, request:Request):
    query = {"name": {"$regex": f"{name}", "$options": "i"}}
    if (ingredients := request.app.database["ingredients"].find(query)) is not None:
        return list(ingredients)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ingredient with name {name} not found")    

@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


@router.put("/{id}", response_description="Update a book", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    book = {k: v for k, v in book.dict().items() if v is not None}

    if len(book) >= 1:
        update_result = request.app.database["books"].update_one(
            {"_id": id}, {"$set": book}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    delete_result = request.app.database["books"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")
