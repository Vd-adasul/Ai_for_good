import os

# Graceful import — faster-whisper may not be installed
try:
    from faster_whisper import WhisperModel
    _WHISPER_AVAILABLE = True
except ImportError:
    _WHISPER_AVAILABLE = False
    print("Warning: faster-whisper not installed. Voice features disabled.")

# Model size can be 'tiny', 'base', 'small', 'medium', 'large-v2'
MODEL_SIZE = "base"

class VoiceService:
    def __init__(self):
        self.model = None
        if not _WHISPER_AVAILABLE:
            print("VoiceService: Whisper not available, voice features disabled.")
            return
        
        print(f"Loading Whisper Model ({MODEL_SIZE})...")
        try:
            self.model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
            print("Whisper Model Loaded.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")

    def transcribe(self, audio_path: str) -> str:
        """Transcribes audio file to text."""
        if not self.model:
            return ""
        
        if not os.path.exists(audio_path):
            return ""

        try:
            segments, info = self.model.transcribe(audio_path, beam_size=5)
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"Transcription Error: {e}")
            return ""

# Global instance
try:
    voice_service = VoiceService()
except Exception:
    voice_service = None
