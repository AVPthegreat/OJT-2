"""
Text-to-Speech Service using Coqui XTTS for voice cloning
"""

from TTS.api import TTS
from typing import Optional
import numpy as np
import io
import os


class TTSService:
    """
    Text-to-Speech service using Coqui XTTS v2 for voice cloning.
    Can generate speech in a cloned voice from just a few minutes of reference audio.
    """
    
    def __init__(
        self,
        model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2",
        reference_audio_path: Optional[str] = None
    ):
        """
        Initialize the TTS model.
        
        Args:
            model_name: The Coqui TTS model to use
            reference_audio_path: Path to the professor's voice recording for cloning
        """
        self.model_name = model_name
        self.reference_audio_path = reference_audio_path
        self.tts: Optional[TTS] = None
        
    def load_model(self):
        """Load the XTTS model"""
        print(f"🔊 Loading XTTS voice cloning model...")
        self.tts = TTS(self.model_name)
        
        # Move to GPU if available
        if self.tts.is_multi_gpu:
            self.tts.to("cuda")
            
        print("✅ XTTS model loaded!")
        
    def set_reference_audio(self, audio_path: str):
        """
        Set the reference audio for voice cloning.
        
        Args:
            audio_path: Path to the professor's voice recording (WAV format, 2-3 mins)
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Reference audio not found: {audio_path}")
            
        self.reference_audio_path = audio_path
        print(f"🎙️ Reference audio set: {audio_path}")
        
    def synthesize(
        self,
        text: str,
        output_path: Optional[str] = None,
        language: str = "en"
    ) -> bytes:
        """
        Synthesize speech from text using the cloned voice.
        
        Args:
            text: The text to convert to speech
            output_path: Optional path to save the audio file
            language: Language code
            
        Returns:
            Audio data as bytes
        """
        if self.tts is None:
            self.load_model()
            
        if self.reference_audio_path is None:
            raise ValueError("Reference audio not set. Call set_reference_audio() first.")
        
        # Generate speech with voice cloning
        if output_path:
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=self.reference_audio_path,
                language=language
            )
            
            # Read the file and return bytes
            with open(output_path, "rb") as f:
                return f.read()
        else:
            # Generate to memory
            wav = self.tts.tts(
                text=text,
                speaker_wav=self.reference_audio_path,
                language=language
            )
            
            # Convert numpy array to bytes
            audio_bytes = np.array(wav, dtype=np.float32).tobytes()
            return audio_bytes
    
    def synthesize_stream(self, text: str, language: str = "en"):
        """
        Stream synthesis for real-time audio generation.
        Yields audio chunks as they're generated.
        
        Args:
            text: Text to synthesize
            language: Language code
            
        Yields:
            Audio chunks as bytes
        """
        if self.tts is None:
            self.load_model()
            
        if self.reference_audio_path is None:
            raise ValueError("Reference audio not set.")
            
        # Split text into sentences for faster streaming
        sentences = text.replace(".", ".|").replace("?", "?|").replace("!", "!|").split("|")
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                wav = self.tts.tts(
                    text=sentence,
                    speaker_wav=self.reference_audio_path,
                    language=language
                )
                yield np.array(wav, dtype=np.float32).tobytes()
