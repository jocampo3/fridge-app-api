from openai._utils import json_safe
from db import SupaClient
from typing import Union, List
from fastapi import APIRouter
from models.products import Product
from datetime import datetime, timezone

router = APIRouter()
db = SupaClient()

@router.post("/products")
def create(product: Product, q: Union[str, None] = None):
    response = db.client.table("products").insert({
        "name": product.name,
        "type": product.type,
        "quantity": product.quantity,
        "store": product.store,
        "stock_location": product.stock_location
    }).execute()

    return response

@router.get("/products/{id}")
def get_product(id: int, q: Union[str, None] = None):
    data = db.client.table("products").select(
        "*").eq("id", id).single().execute()
    return data

@router.get("/products")
def get_products():
    data = db.client.table("products").select(
        "*").is_("discarded_at", None).order("created_at", desc=True).execute()
    return data

@router.put("/products/{id}")
def update_product(id: int, product: Product, q: Union[str, None] = None):
    response = db.client.table("products").update({
        "name": product.name,
        "type": product.type,
        "quantity": product.quantity,
        "store": product.store,
        "discarded_at": product.discarded_at,
        "stock_location": product.stock_location
    }).eq("id", id).execute()
    return response


@router.delete("/products/{id}")
def delete_product(id: int, q: Union[str, None] = None):
    time = datetime.now(timezone.utc)
    timestamp = time.isoformat()
    response = db.client.table("products").update(
        {"discarded_at": timestamp}).eq("id", id).execute()
    return response

def parse_recipes(response: str):
    import json

    try:
        data = json.loads(response)
        return data["recipes"]

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned from model",
            "raw": response
        }

    except KeyError:
        return {
            "error": "Missing recipes field",
            "raw": response
        }

@router.post("/products/recipes")
def get_recipes(products: List[str]):
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        text={
            "format": {
                "type": "json_schema",
                "name": "recipes",
                "schema": {
                    "type": "object",
                    "properties": {
                        "recipes": {
                            "type": "array",
                            "minItems": 6,
                            "maxItems": 6,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "recipe": {"type": "string"}
                                },
                                "required": ["name", "recipe"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["recipes"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        model="gpt-4o",
        instructions = """
        You are a world-class Michelin 5-star chef who specializes in creative and exotic cuisine.

        Your task is to generate recipe ideas based on the provided product information.

        For the given products, create **six recipes**:
        - Two breakfast recipe
        - Two lunch recipe
        - Two dinner recipe

        Each recipe should:
        - Use the provided product as a main or featured ingredient
        - Be creative but realistic
        - Include detailed ingredients and preparation steps
        - Include measurements when possible
        - Include seasoning information
        - Include any additional preparation processes if required (examples: breading, marinades, sauces, salsas, reductions, etc.)

        Recipes must be **highly detailed**, specific, and written clearly enough that someone could follow them to cook the dish.

### Output Format Requirements

        Return the response **ONLY as valid JSON**.

        The JSON format must be an **array of objects**, where:
        - The **key** is the recipe name
        - The **value** is the full recipe description

        Example format:

        [
            {
                "Chilaquiles Verdes with Braised Chicken": "Ingredients: 4 eggs, 10 corn tortillas, 1 cup shredded chicken, 1 cup salsa verde, 1/2 cup queso fresco, 1/4 cup diced onion, 1 avocado sliced. Seasonings: 1 tsp salt, 1/2 tsp black pepper, 1/2 tsp cumin. Instructions: Cut tortillas into triangles and lightly fry until crispy. Heat salsa verde in a skillet and toss tortillas until coated. Add shredded chicken and simmer for 3 minutes. Fry eggs separately and place on top. Garnish with queso fresco, onion, and avocado."
            },
            {
                "Spicy Crispy Chicken Sandwich": "Ingredients: 2 chicken breasts, 2 brioche buns, dill pickles, 1 cup flour, 1 egg, 1 cup buttermilk. Seasonings: 1 tsp paprika, 1/2 tsp cayenne pepper, 1 tsp garlic powder, 1 tsp salt, 1/2 tsp black pepper. Instructions: Pound chicken breasts evenly. Create a breading station with flour and seasonings, then egg and buttermilk mixture. Dredge chicken in flour, dip in wet mixture, then dredge again. Fry at 350°F until golden brown. Toast brioche buns and assemble with pickles and spicy mayo."
            }
        ]

        Important Rules:
        - Return **exactly six recipes**
        - Two must be breakfast, two lunch, two dinner
        - Output **only valid JSON**
        - Do **not include explanations outside the JSON**
        """,
        input=f"{products}"
    )

    if response.status == "completed":
        recipes = parse_recipes(response.output_text)
        return {"output": recipes, "status_code": 200}
    else:
        return {"output": "Could not generate recipes", "status_code": 400}


