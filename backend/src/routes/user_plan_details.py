from fastapi import APIRouter, HTTPException
from src.db.mongo_client import db


user_plan_details_router = APIRouter()


@user_plan_details_router.post("/users/{user_id}/plans")
async def create_user_plan_detail(user_id: str, plan_detail: dict):
    plan_detail["user_id"] = user_id
    plan_detail["status"]="intitiated"
    await db["user_plan_details"].insert_one(plan_detail)
    return {"message": "User plan detail added successfully!"}


async def create_user_plan_detail_internal(user_id: str, plan_detail: dict):
    plan_detail["user_id"] = user_id
    await db["user_plan_details"].insert_one(plan_detail)

async def update_user_plan_details(user_id:str, updates:dict):
    result=await db["user_plan_details"].update_one(
        {"user_id":user_id},
        {"$set":updates}
    )
    if result.matched_count==0:
        raise HTTPException(status_code=404, detail="User plan details not found")
    return {"message":"User plan details updated successfully!"}    