from db import SupaClient
from typing import Union
from fastapi import APIRouter
from models import Product
from datetime import datetime, timezone

router = APIRouter()
db = SupaClient()


@router.get("/products")
def get_products():
    data = db.client.table("products").select(
        "*").is_("discarded_at", None).order("created_at", desc=True).execute()
    return data


@router.post("/products")
def create(product: Product, q: Union[str, None] = None):
    response = db.client.table("products").insert({
        "name": product.name,
        "type": product.type,
        "quantity": product.quantity,
        "store": product.store,
    }).execute()

    return response


@router.get("/products/{id}")
def read(id: int, q: Union[str, None] = None):
    data = db.client.table("products").select(
        "*").eq("id", id).single().execute()
    return data


@router.put("/products/{id}")
def update(id: int, product: Product, q: Union[str, None] = None):
    response = db.client.table("products").update({
        "name": product.name,
        "type": product.type,
        "quantity": product.quantity,
        "store": product.store,
        "discarded_at": product.discarded_at
    }).eq("id", id).execute()
    return response


@router.delete("/products/{id}")
def delete(id: int, q: Union[str, None] = None):
    time = datetime.now(timezone.utc)
    timestamp = time.isoformat()
    response = db.client.table("products").update(
        {"discarded_at": timestamp}).eq("id", id).execute()
    return response
    # response = db.client.table("products").delete().eq("id", id).execute()
    # return response
