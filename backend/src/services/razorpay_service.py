import razorpay, os, hmac,hashlib
from fastapi.concurrency import run_in_threadpool

razorpay_client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))

async def create_order(amount:int,currency:str="INR"):
    def blocking_create():
        return razorpay_client.order.create({
            "amount": amount * 100,  # Amount in paise  
            "currency": currency,
             "receipt": "receipt_001"
        })
    order = await run_in_threadpool(blocking_create)
    return order


def verify_payment_signature(razorpay_order_id:str, razorpay_payment_id:str, razorpay_signature:str)->bool:
    expected=hmac.new(
        os.getenv("RAZORPAY_KEY_SECRET").encode(),
        f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
        hashlib.sha256
    ).hexdigest()

    return expected == razorpay_signature 
