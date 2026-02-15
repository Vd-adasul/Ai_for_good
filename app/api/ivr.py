from fastapi import APIRouter, Request, BackgroundTasks
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.core.voice import voice_service
import requests
import os
import uuid

router = APIRouter()

@router.post("/welcome")
async def welcome(request: Request):
    """Handle incoming call."""
    resp = VoiceResponse()
    
    # 1. Ask for District
    resp.say("नमस्ते! कृपया आपला जिल्हा सांगा.", language="mr-IN", voice="Polly.Aditi")
    
    # Simple Record for now
    resp.record(max_length=10, action="/ivr/handle_district")
    
    return str(resp)

@router.post("/handle_district")
async def handle_district(request: Request):
    """Process district recording."""
    resp = VoiceResponse()
    # In real implementation: Transcribe audio -> Extract District
    # For MVP, just acknowledge
    
    resp.say("धन्यवाद. आता आपली समस्या किंवा प्रश्न सांगा.", language="mr-IN", voice="Polly.Aditi")
    resp.record(max_length=30, action="/ivr/handle_question")
    
    return str(resp)

@router.post("/handle_question")
async def handle_question(request: Request, background_tasks: BackgroundTasks):
    """Process question recording."""
    resp = VoiceResponse()
    
    # Get Recording URL
    form_data = await request.form()
    recording_url = form_data.get("RecordingUrl")
    
    transcribed_text = ""
    if recording_url and voice_service:
        try:
            # Download audio
            r = requests.get(recording_url)
            if r.status_code == 200:
                filename = f"temp_ivr_{uuid.uuid4()}.wav"
                with open(filename, 'wb') as f:
                    f.write(r.content)
                
                # Transcribe
                transcribed_text = voice_service.transcribe(filename)
                
                # Cleanup
                if os.path.exists(filename):
                    os.remove(filename)
        except Exception as e:
            print(f"IVR Voice Error: {e}")

    if transcribed_text:
        resp.say(f"आम्ही ऐकले: {transcribed_text}. आम्ही याचे उत्तर लवकरच तुम्हाला पाठवू.", language="mr-IN", voice="Polly.Aditi")
    else:
        resp.say("आम्हाला तुमचा आवाज ऐकू आला नाही. कृपया पुन्हा प्रयत्न करा.", language="mr-IN", voice="Polly.Aditi")
    
    resp.hangup()
    return str(resp)
