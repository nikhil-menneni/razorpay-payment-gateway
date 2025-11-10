from pydantic import BaseModel, Field
from datetime import datetime

class Subscription(BaseModel):
    user_id:str
    plan_id:str
    start_date:datetime=Field(default_factory=datetime.utcnow)
    end_date:datetime
    status:str="active"