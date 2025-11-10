from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Payment(BaseModel):
    razorpay_order_id:str=Field(..., description="Razorpay Order ID")
    razorpay_payment_id:Optional[str]=Field(None, description="Razorpay Payment ID")
    amount:int
    currency:str="INR"
    status: str = "initiated" 
    created_at:datetime=Field(default_factory=datetime.utcnow)

    