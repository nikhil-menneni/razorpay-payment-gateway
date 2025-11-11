from fastapi import APIRouter, BackgroundTasks, HTTPException
from src.services.razorpay_service import create_order, verify_payment_signature
from src.db.mongo_client import db
from pydantic import BaseModel
# from src.services.razorpay_service import download_invoice_pdf
from src.services.razorpay_service import download_and_save_invoice_pdf
from src.routes.user_plan_details import create_user_plan_detail_internal
from src.routes.user_plan_details import update_user_plan_details
from datetime import datetime

paymentRouter = APIRouter()

class CreateOrderRequest(BaseModel):
    amount: int

@paymentRouter.post("/create-order")
async def create_payment_order(payload: CreateOrderRequest):
    order= await create_order(payload.amount)
    await db["payments"].insert_one({
        "razorpay_order_id": order["id"],
        "amount": payload.amount,
        "status":"Initiated",
        "user_id": "some_user_id"  # Replace with actual user ID
    })

    await create_user_plan_detail_internal(
        user_id="some_user_id",  # Replace with actual user ID
        plan_detail={
            "plan_id": "some_plan_id",  # Replace with actual plan ID
            "start_date": None,
            "end_date": None,
            "status": "pending"
        })

    return {"order_id": order["id"], "amount": payload.amount}

@paymentRouter.post("/verify")
async def verify_payment(data:dict,background_tasks:BackgroundTasks):
    order_id=data.get("razorpay_order_id")
    payment_id=data.get("razorpay_payment_id")
    signature=data.get("razorpay_signature")
    user_id=data.get("user_id")

    if not verify_payment_signature(order_id, payment_id, signature):
        raise HTTPException(status_code=400, detail="Invalid payment signature")
    
    await db["payments"].update_one(
        {"razorpay_order_id": order_id},
        {"$set":{"razorpay_payment_id": payment_id, "status":"Completed"}})
    
    await update_user_plan_details(
        user_id=user_id,
        updates={"status":"active"}
    )
    
    await download_and_save_invoice_pdf(payment_id)
    
    background_tasks.add_task(download_and_save_invoice_pdf, payment_id)

    return {"message": "Payment verified successfully!"}

@paymentRouter.post("/failed")
async def payment_failed(data:dict):
    print("data",data)
    order_id=data.get("razorpay_order_id")
    reason=data.get("reason","Unknown")
    code=data.get("code","N/A")

    await db["payments"].update_one(
        {"razorpay_order_id": order_id},
        {"$set":{"status":"Failed", "failure_reason": reason, "failure_code": code}, "$inc":{"retry_count":1}}
    )

    return {"message":f"Marked order {order_id} as failed","reason":reason}


@paymentRouter.post("/closed")
async def payment_closed(data:dict):
    order_id = data["order_id"]
    await db["payments"].update_one(
        
            {"razorpay_order_id": order_id},
            {"$set":{"status": "abandoned", "closed_at": datetime.utcnow()}}
        
    )
    return {"message":f"User closed payment window for order {order_id}"} 



async def log_payment_event(order_id:str, payment_id:str):
    await db["payment_logs"].insert_one({
        "order_id": order_id,
        "payment_id": payment_id
    })