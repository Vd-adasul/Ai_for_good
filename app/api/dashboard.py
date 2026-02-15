from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from app.core.weather import weather_service
from app.core.market import market_service
from app.core.subsidy import subsidy_service
from app.core.rag import rag_engine

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    district: str = "Maharashtra"
    history: List[dict] = [] # List of {role: 'user'|'ai', content: '...'}

class ChatResponse(BaseModel):
    response: str
    context_used: Optional[str] = None

@router.get("/weather")
async def get_weather(city: str):
    """Get weather for a specific city."""
    weather = weather_service.get_weather(city)
    if not weather:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return weather

@router.get("/prices")
async def get_prices():
    """Get market prices for key crops."""
    # Hardcoded for now based on code.html context, ideally fetched from DB/API
    commodities = ["soybean", "cotton", "gram", "pigeon pea"]
    prices = []
    for comm in commodities:
        price = market_service.get_price(comm)
        if price:
            # Mocking trend for now as market_service might not have it
            prices.append({
                "commodity": comm.title(),
                "price": price,
                "change": "+ ₹120 this week" if comm == "soybean" else "Stable"
            })
    return prices

@router.get("/subsidies")
async def get_subsidies(category: Optional[str] = None):
    """Get subsidy schemes."""
    if category:
        return subsidy_service.get_schemes_by_category(category)
    return subsidy_service.get_all_schemes()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI Agri Advisor."""
    try:
        # 1. Enrich context with weather
        weather_info = weather_service.get_weather(request.district)
        weather_context = ""
        if weather_info:
            weather_context = f"Current weather in {request.district}: {weather_info['weather']}, Temp: {weather_info['temp']}C."

        # 2. Enrich context with prices (basic)
        price_info = ""
        # We could inject prices relevant to the query if we did intent analysis, 
        # but for now, let's keep it simple or just let RAG handle it if it has access to tool data.
        # For this prototype, we'll just pass the district context.
        
        # 3. RAG Query
        # We pass the constructed context to the RAG engine
        
        context = f"District: {request.district}. {weather_context}"
        
        answer = rag_engine.get_answer(request.message, context, history=request.history)
        
        return ChatResponse(response=answer, context_used=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
