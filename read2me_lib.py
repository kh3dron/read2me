"""
Read2Me Library - Simple library for audiobook generation
Designed for integration with web applications
"""

import os
import json
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Callable
import torch
from TTS.api import TTS

class AudiobookGenerator:
    """Main class for generating audiobooks from text"""
    
    def __init__(self, output_dir: str = "output", model: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = model
        self.tts = None
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.voice_samples_dir = Path("voice_samples")
        
    def _init_tts(self):
        """Initialize TTS model (lazy loading)"""
        if self.tts is None:
            self.tts = TTS(self.model).to(self.device)
    
    def get_available_voices(self) -> List[str]:
        """Get list of available built-in voices"""
        if not self.voice_samples_dir.exists():
            return []
        
        voices = []
        for voice_file in self.voice_samples_dir.glob("*.wav"):
            voices.append(voice_file.stem)
        return sorted(voices)
    
    def generate_audio(self, 
                      text: str, 
                      voice: Optional[str] = None,
                      voice_file: Optional[str] = None,
                      language: str = "en",
                      output_filename: Optional[str] = None,
                      progress_callback: Optional[Callable[[str], None]] = None) -> str:
        """
        Generate audio from text
        
        Args:
            text: Text to synthesize
            voice: Built-in voice name
            voice_file: Path to voice sample for cloning
            language: Language code
            output_filename: Custom output filename
            progress_callback: Function to call with progress updates
            
        Returns:
            Path to generated audio file
        """
        self._init_tts()
        
        if progress_callback:
            progress_callback("Initializing TTS...")
        
        # Generate output filename
        if not output_filename:
            task_id = str(uuid.uuid4())[:8]
            output_filename = f"audio_{task_id}.wav"
        
        output_path = self.output_dir / output_filename
        
        try:
            if progress_callback:
                progress_callback("Generating audio...")
            
            if voice_file:
                # Voice cloning
                self.tts.tts_to_file(
                    text=text,
                    speaker_wav=voice_file,
                    file_path=str(output_path),
                    language=language
                )
            elif voice:
                # Built-in voice
                self.tts.tts_to_file(
                    text=text,
                    file_path=str(output_path),
                    speaker=voice,
                    language=language,
                    split_sentences=True
                )
            else:
                # Default voice
                self.tts.tts_to_file(
                    text=text,
                    file_path=str(output_path),
                    speaker="Ana Florence",
                    language=language,
                    split_sentences=True
                )
            
            if progress_callback:
                progress_callback("Audio generation complete")
            
            return str(output_path)
            
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error: {e}")
            raise e
    
    def create_audiobook(self,
                        text: str,
                        title: str,
                        voice: Optional[str] = None,
                        voice_file: Optional[str] = None,
                        language: str = "en",
                        max_chapter_length: int = 10000,
                        progress_callback: Optional[Callable[[str], None]] = None) -> Dict:
        """
        Create a complete audiobook from text
        
        Args:
            text: Full book text
            title: Book title for output directory
            voice: Built-in voice name
            voice_file: Path to voice sample for cloning
            language: Language code
            max_chapter_length: Maximum characters per chapter
            progress_callback: Function to call with progress updates
            
        Returns:
            Dictionary with audiobook metadata
        """
        if progress_callback:
            progress_callback("Starting audiobook creation...")
        
        # Create book output directory
        book_dir = self.output_dir / title.replace(" ", "_")
        book_dir.mkdir(parents=True, exist_ok=True)
        
        # Split text into chapters
        chapters = self._split_text(text, max_chapter_length)
        total_chapters = len(chapters)
        
        if progress_callback:
            progress_callback(f"Split into {total_chapters} chapters")
        
        # Generate audio for each chapter
        audio_files = []
        for i, chapter_text in enumerate(chapters, 1):
            if progress_callback:
                progress_callback(f"Processing chapter {i}/{total_chapters}")
            
            chapter_filename = f"chapter_{i:02d}.wav"
            chapter_path = book_dir / chapter_filename
            
            audio_path = self.generate_audio(
                text=chapter_text,
                voice=voice,
                voice_file=voice_file,
                language=language,
                output_filename=chapter_path.name,
                progress_callback=None  # Avoid nested callbacks
            )
            
            # Move to book directory if needed
            if Path(audio_path).parent != book_dir:
                final_path = book_dir / chapter_filename
                Path(audio_path).rename(final_path)
                audio_path = str(final_path)
            
            audio_files.append({
                "chapter": i,
                "filename": chapter_filename,
                "path": audio_path,
                "duration": None  # Could be calculated if needed
            })
        
        # Create metadata
        metadata = {
            "title": title,
            "total_chapters": total_chapters,
            "voice_used": voice or "voice_clone" if voice_file else "Ana Florence",
            "language": language,
            "output_directory": str(book_dir),
            "audio_files": audio_files,
            "created_at": str(Path().ctime())
        }
        
        # Save metadata
        metadata_file = book_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        if progress_callback:
            progress_callback("Audiobook creation complete")
        
        return metadata
    
    def create_audiobook_from_file(self,
                                  file_path: str,
                                  voice: Optional[str] = None,
                                  voice_file: Optional[str] = None,
                                  language: str = "en",
                                  progress_callback: Optional[Callable[[str], None]] = None) -> Dict:
        """
        Create audiobook from a text file
        
        Args:
            file_path: Path to text file
            voice: Built-in voice name
            voice_file: Path to voice sample for cloning
            language: Language code
            progress_callback: Function to call with progress updates
            
        Returns:
            Dictionary with audiobook metadata
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if progress_callback:
            progress_callback("Reading input file...")
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")
        
        if not text.strip():
            raise ValueError("File is empty")
        
        # Use filename as title
        title = file_path.stem
        
        return self.create_audiobook(
            text=text,
            title=title,
            voice=voice,
            voice_file=voice_file,
            language=language,
            progress_callback=progress_callback
        )
    
    def _split_text(self, text: str, max_length: int) -> List[str]:
        """Split text into chapters based on length and natural breaks"""
        # Split by double newlines (paragraphs) first
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        chapters = []
        current_chapter = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed max length
            if current_chapter and len(current_chapter) + len(paragraph) + 2 > max_length:
                chapters.append(current_chapter.strip())
                current_chapter = paragraph
            else:
                if current_chapter:
                    current_chapter += "\n\n" + paragraph
                else:
                    current_chapter = paragraph
        
        # Add the last chapter
        if current_chapter.strip():
            chapters.append(current_chapter.strip())
        
        return chapters

# Convenience functions for simple usage
def quick_tts(text: str, voice: str = None, output_file: str = None) -> str:
    """Quick TTS generation function"""
    generator = AudiobookGenerator()
    return generator.generate_audio(text=text, voice=voice, output_filename=output_file)

def book_to_audio(file_path: str, voice: str = None, progress_callback=None) -> Dict:
    """Convert book file to audiobook"""
    generator = AudiobookGenerator()
    return generator.create_audiobook_from_file(
        file_path=file_path,
        voice=voice,
        progress_callback=progress_callback
    )