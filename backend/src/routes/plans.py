from fastapi import APIRouter
from src.db.mongo_client import db
from src.models.plan_model import Plan

planRouter = APIRouter()

@planRouter.get("/")
async def get_plans():
    plans=await db["plans"].find().to_list(20)
    return {"plans": plans}

@planRouter.post("/")
async def create_plan(plan: Plan):
    await db["plans"].insert_one(plan.model_dump())
    return {"message": "Plan added successfully!"}
