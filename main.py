from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import whatsapp, ivr, admin
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI for Good - Farmer Bot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI for Good Backend is running!"}

app.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
app.include_router(whatsapp.router, prefix="", tags=["WhatsApp"])  # Also serve at /bot for Twilio
app.include_router(ivr.router, prefix="/ivr", tags=["IVR"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
from app.api import dashboard
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
