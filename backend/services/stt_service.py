"""
Speech-to-Text Service using Faster Whisper
"""

from faster_whisper import WhisperModel
import numpy as np
from typing import Optional, Tuple
import io


class STTService:
    """
    Speech-to-Text service using Faster Whisper for efficient transcription.
    """
    
    def __init__(
        self,
        model_size: str = "base",
        device: str = "auto",
        compute_type: str = "float16"
    ):
        """
        Initialize the Whisper model.
        
        Args:
            model_size: Size of model - tiny, base, small, medium, large-v2, large-v3
            device: "cuda" or "cpu" or "auto"
            compute_type: "float16", "int8", "float32"
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model: Optional[WhisperModel] = None
        
    def load_model(self):
        """Load the Whisper model into memory"""
        print(f"🎤 Loading Whisper {self.model_size} model...")
        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type
        )
        print("✅ Whisper model loaded!")
        
    def transcribe(
        self,
        audio_data: bytes,
        language: str = "en"
    ) -> Tuple[str, float]:
        """
        Transcribe audio bytes to text.
        
        Args:
            audio_data: Raw audio bytes (WAV format expected)
            language: Language code (default: English)
            
        Returns:
            Tuple of (transcribed_text, confidence_score)
        """
        if self.model is None:
            self.load_model()
            
        # Convert bytes to numpy array for faster-whisper
        audio_array = np.frombuffer(audio_data, dtype=np.float32)
        
        segments, info = self.model.transcribe(
            audio_array,
            language=language,
            beam_size=5,
            vad_filter=True,  # Voice activity detection
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=200
            )
        )
        
        # Combine all segments
        full_text = ""
        total_confidence = 0.0
        segment_count = 0
        
        for segment in segments:
            full_text += segment.text + " "
            total_confidence += segment.avg_logprob
            segment_count += 1
            
        avg_confidence = total_confidence / max(segment_count, 1)
        
        return full_text.strip(), avg_confidence
    
    def transcribe_stream(self, audio_chunk: bytes) -> str:
        """
        Transcribe a streaming audio chunk.
        Used for real-time transcription during interview.
        
        Args:
            audio_chunk: Small audio chunk (e.g., 1 second)
            
        Returns:
            Transcribed text for this chunk
        """
        if self.model is None:
            self.load_model()
            
        audio_array = np.frombuffer(audio_chunk, dtype=np.float32)
        
        segments, _ = self.model.transcribe(
            audio_array,
            language="en",
            beam_size=1,  # Faster for streaming
            without_timestamps=True
        )
        
        return " ".join(segment.text for segment in segments)
