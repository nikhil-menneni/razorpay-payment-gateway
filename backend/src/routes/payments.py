from fastapi import APIRouter, BackgroundTasks, HTTPException
from src.services.razorpay_service import create_order, verify_payment_signature
from src.db.mongo_client import db

paymentRouter = APIRouter()

@paymentRouter.post("/create-order")
async def create_payment_order(amount: int):
    order= await create_order(amount)
    await db["payments"].insert_one({
        "razorpay_order_id": order["id"],
        "amount": amount,
        "status":"Initiated"
    })

    return {"order_id": order["id"], "amount": amount}

@paymentRouter.post("/verify-payment")
async def verify_payment(data:dict,background_tasks:BackgroundTasks):
    order_id=data.get("razorpay_order_id")
    payment_id=data.get("razorpay_payment_id")
    signature=data.get("razorpay_signature")

    if not verify_payment_signature(order_id, payment_id, signature):
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    
    await db["payments"].update_one(
        {"razorpay_order_id": order_id},
        {"$set":{"razorpay_payment_id": payment_id, "status":"Completed"}})
    
    background_tasks.add_task(log_payment_event, order_id, payment_id)

    return {"message": "Payment verified successfully!"}

async def log_payment_event(order_id:str, payment_id:str):
    await db["payment_logs"].insert_one({
        "order_id": order_id,
        "payment_id": payment_id
    })