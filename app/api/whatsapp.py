from fastapi import APIRouter, Request, BackgroundTasks, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.core.rag import rag_engine
from app.core.weather import weather_service
from app.core.market import market_service
from app.core.voice import voice_service
import requests
import os
import uuid

router = APIRouter()

# Simple in-memory state for MVP (use Redis/Database for prod)
user_state = {}
user_data = {}

@router.get("/bot")
async def bot_verify():
    """Webhook verification endpoint."""
    return {"status": "WhatsApp bot webhook is active"}

@router.post("/bot")
async def bot(request: Request, background_tasks: BackgroundTasks):
    """WhatsApp Webhook Handler."""
    form_data = await request.form()
    incoming_msg = form_data.get("Body", "").strip()
    sender = form_data.get("From")
    media_url = form_data.get("MediaUrl0")
    media_type = form_data.get("MediaContentType0", "")

    print(f"\n{'='*50}")
    print(f"[WHATSAPP] Incoming message from: {sender}")
    print(f"[WHATSAPP] Message body: '{incoming_msg}'")
    print(f"[WHATSAPP] State: {user_state.get(sender, 'NEW USER')}")
    print(f"{'='*50}")

    resp = MessagingResponse()
    msg = resp.message()

    # Handle Voice Note
    if media_url and media_type and "audio" in media_type:
        if not voice_service:
            msg.body("आवाज सेवा सध्या उपलब्ध नाही. कृपया मजकूर पाठवा.")
            return Response(content=str(resp), media_type="application/xml")

        msg.body("तुमचा आवाज मिळाला आहे. प्रक्रिया सुरू आहे...")
        
        try:
            # Download audio
            r = requests.get(media_url)
            if r.status_code == 200:
                filename = f"temp_{uuid.uuid4()}.ogg"
                with open(filename, 'wb') as f:
                    f.write(r.content)
                
                # Transcribe
                transcribed_text = voice_service.transcribe(filename)
                
                # Cleanup
                if os.path.exists(filename):
                    os.remove(filename)

                if not transcribed_text:
                    msg.body("आवाज ओळखता आला नाही. कृपया पुन्हा प्रयत्न करा.")
                    return Response(content=str(resp), media_type="application/xml")

                # Treat transcribed text as incoming message
                incoming_msg = transcribed_text
            else:
                msg.body("आवाज डाउनलोड करण्यात त्रुटी आली.")
                return Response(content=str(resp), media_type="application/xml")
        except Exception as e:
            print(f"Voice Error: {e}")
            msg.body("आवाजावर प्रक्रिया करताना त्रुटी आली.")
            return Response(content=str(resp), media_type="application/xml")

    # Basic State Machine
    if sender not in user_state:
        # Default starting state
        user_state[sender] = "ASK_PLACE"
        # Initialize user data with empty history
        user_data[sender] = {"history": []}
        msg.body("नमस्ते! मी तुमचा कृषी सहाय्यक आहे.\n\nतुम्ही कोणत्या जिल्ह्यात आहात? (उदा. बीड, लातूर)")
        return Response(content=str(resp), media_type="application/xml")

    if user_state[sender] == "ASK_PLACE":
        # Capture District
        district = incoming_msg.title()
        user_data[sender]["place"] = district
        user_state[sender] = "READY"
        msg.body(f"धन्यवाद! {district} निवडले.\n\nआता तुमची समस्या किंवा प्रश्न विचारा. (उदा. दुष्काळात सोयाबीनचे नियोजन कसे करावे?)")
        return Response(content=str(resp), media_type="application/xml")

    if user_state[sender] == "READY":
        # RAG Flow
        district = user_data[sender].get("place", "Maharashtra")
        history = user_data[sender].get("history", [])
        
        # 1. Weather Injection
        weather_info = weather_service.get_weather(district)
        weather_context = ""
        if weather_info:
            weather_context = f"Current weather in {district}: {weather_info['weather']}, Temp: {weather_info['temp']}C."

        # 2. Market Prices Injection
        price_info = ""
        crops_map = {
            "soybean": ["soybean", "soya", "सोयाबीन"],
            "cotton": ["cotton", "kapus", "कापूस"],
            "gram": ["gram", "chana", "chan", "हरभरा"],
            "pigeon pea": ["pigeon pea", "tur", "toor", "तूर"]
        }

        for crop_key, keywords in crops_map.items():
            if any(k in incoming_msg.lower() for k in keywords):
                price = market_service.get_price(crop_key)
                if price:
                    # Translate crop name for display
                    marathi_crop = {
                        "soybean": "सोयाबीन",
                        "cotton": "कापूस",
                        "gram": "हरभरा", 
                        "pigeon pea": "तूर"
                    }.get(crop_key, crop_key)
                    price_info += f"\n{marathi_crop}चा सध्याचा भाव: ₹{price}/क्विंटल."

        # 3. RAG Query
        context = f"District: {district}. {weather_context} {price_info}"
        
        # Get answer with history
        answer = rag_engine.get_answer(incoming_msg, context, history=history)
        
        # Update history
        history.append({"role": "user", "content": incoming_msg})
        history.append({"role": "ai", "content": answer})
        
        # Keep history manageable (last 10 turns)
        if len(history) > 10:
            history = history[-10:]
        
        user_data[sender]["history"] = history
        
        # Append Price info to answer if relevant
        final_response = f"{answer}\n{price_info}" if price_info else answer
        
        msg.body(final_response)
        return Response(content=str(resp), media_type="application/xml")

    return Response(content=str(resp), media_type="application/xml")
