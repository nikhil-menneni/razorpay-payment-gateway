from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Plan(BaseModel):
    id:str=Field(..., description="Plan ID, e.g. GOLD, PLATINUM")
    name:str
    price:int=Field(..., description="Price in paise (e.g. 99900)")
    currenct:str="INR"
    duration_months:int=1
    features:Optional[List[str]]=Field(default_factory=list)
    created_at:datetime=Field(default_factory=datetime.utcnow)