from fastapi import APIRouter
from src.db.mongo_client import db
from src.models.plan_model import Plan

from datetime import datetime

planRouter = APIRouter()

@planRouter.get("/")
async def get_plans():
    plans=await db["plans"].find().to_list(20)
    for plan in plans:
        plan["_id"]=str(plan["_id"])
    return {"plans": plans}

@planRouter.post("/")
async def create_plan(plan: Plan):
    await db["plans"].insert_one(plan.model_dump())
    return {"message": "Plan added successfully!"}

@planRouter.post("/seed")
async def seed_plans():
    await db.plans.create_index("name", unique=True)
    sample_plans = [
        {
            "id": "BASIC",
            "name": "Basic Plan",
            "price": 499,
            "currency": "INR",
            "duration_months": 1,
            "max_employees": 1,
            "features": [
                "Access to basic content",
                "Standard support",
                "Single device access"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "GOLD",
            "name": "Gold Plan",
            "price": 999,
            "currency": "INR",
            "duration_months": 3,
            "max_employees": 5,
            "features": [
                "Priority support",
                "Multi-device access",
                "Early access to new features"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "PLATINUM",
            "name": "Platinum Plan",
            "price": 1999,
            "currency": "INR",
            "duration_months": 6,
            "max_employees": 10,
            "features": [
                "Dedicated account manager",
                "Advanced analytics dashboard",
                "Custom reports",
                "Exclusive beta access"
            ],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]

    await db["plans"].insert_many(sample_plans)
    return {"message": "Sample plans seeded successfully!"}

