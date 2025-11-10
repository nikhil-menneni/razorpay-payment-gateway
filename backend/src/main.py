from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import router


app=FastAPI(title="Razorpay Payment Gateway Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Razorpay Payment Gateway Backend"}