import os

# Voice/Whisper features are disabled to save memory on limited-RAM deployments.
# The faster-whisper model requires ~150MB+ RAM which exceeds our budget.

class VoiceService:
    def __init__(self):
        self.model = None
        print("VoiceService: Voice transcription is disabled (memory-limited deployment).")

    def transcribe(self, audio_path: str) -> str:
        """Transcribes audio file to text. Currently disabled."""
        return ""

# Global instance — always None-like (no model loaded)
voice_service = VoiceService()
