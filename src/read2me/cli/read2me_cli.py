#!/usr/bin/env python3
"""
Read2Me CLI - Simple command-line interface for audiobook generation
"""

import argparse
import os
import sys
import json
import uuid
from pathlib import Path
import torch
from TTS.api import TTS

class Read2MeCLI:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = "tts_models/multilingual/multi-dataset/xtts_v2"
        self.tts = None
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
    def _init_tts(self):
        """Initialize TTS model (lazy loading)"""
        if self.tts is None:
            print(f"Loading TTS model on {self.device}...")
            self.tts = TTS(self.model).to(self.device)
    
    def list_voices(self):
        """List available built-in voices"""
        voice_samples_dir = Path("voice_samples")
        if not voice_samples_dir.exists():
            print("No voice samples directory found")
            return []
        
        voices = []
        for voice_file in voice_samples_dir.glob("*.wav"):
            voices.append(voice_file.stem)
        
        print("Available voices:")
        for voice in sorted(voices):
            print(f"  - {voice}")
        return voices
    
    def generate_tts(self, text, voice=None, voice_file=None, output_file=None, language="en"):
        """Generate TTS audio from text"""
        self._init_tts()
        
        if not output_file:
            task_id = str(uuid.uuid4())[:8]
            output_file = self.output_dir / f"audiobook_{task_id}.wav"
        else:
            output_file = Path(output_file)
        
        try:
            if voice_file:
                # Voice cloning
                print(f"Cloning voice from: {voice_file}")
                self.tts.tts_to_file(
                    text=text,
                    speaker_wav=voice_file,
                    file_path=str(output_file),
                    language=language
                )
            elif voice:
                # Built-in voice
                print(f"Using built-in voice: {voice}")
                self.tts.tts_to_file(
                    text=text,
                    file_path=str(output_file),
                    speaker=voice,
                    language=language,
                    split_sentences=True
                )
            else:
                # Default voice
                print("Using default voice: Ana Florence")
                self.tts.tts_to_file(
                    text=text,
                    file_path=str(output_file),
                    speaker="Ana Florence",
                    language=language,
                    split_sentences=True
                )
            
            print(f"Audio generated successfully: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None
    
    def process_book(self, input_file, voice=None, voice_file=None, output_dir=None, language="en"):
        """Process a book file into audiobook"""
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"Input file not found: {input_file}")
            return None
        
        # Read input text
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}")
            return None
        
        if not text.strip():
            print("Input file is empty")
            return None
        
        # Set output directory
        if output_dir:
            book_output_dir = Path(output_dir)
        else:
            book_output_dir = self.output_dir / input_path.stem
        
        book_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Split into chapters if text is very long
        max_chunk_size = 10000  # characters
        if len(text) > max_chunk_size:
            print(f"Large book detected ({len(text)} chars). Splitting into chapters...")
            chapters = self._split_into_chapters(text, max_chunk_size)
        else:
            chapters = [text]
        
        # Generate audio for each chapter
        audio_files = []
        for i, chapter_text in enumerate(chapters, 1):
            chapter_file = book_output_dir / f"chapter_{i:02d}.wav"
            print(f"Processing chapter {i}/{len(chapters)}...")
            
            result = self.generate_tts(
                text=chapter_text,
                voice=voice,
                voice_file=voice_file,
                output_file=chapter_file,
                language=language
            )
            
            if result:
                audio_files.append(result)
            else:
                print(f"Failed to generate chapter {i}")
        
        # Create metadata file
        metadata = {
            "book_title": input_path.stem,
            "total_chapters": len(chapters),
            "voice_used": voice or "voice_clone" if voice_file else "Ana Florence",
            "language": language,
            "audio_files": audio_files
        }
        
        metadata_file = book_output_dir / "metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Audiobook generated in: {book_output_dir}")
        print(f"Total chapters: {len(audio_files)}")
        return str(book_output_dir)
    
    def _split_into_chapters(self, text, max_size):
        """Split text into manageable chunks"""
        # Simple splitting by paragraphs, respecting max size
        paragraphs = text.split('\n\n')
        chapters = []
        current_chapter = ""
        
        for paragraph in paragraphs:
            if len(current_chapter) + len(paragraph) > max_size and current_chapter:
                chapters.append(current_chapter.strip())
                current_chapter = paragraph
            else:
                current_chapter += "\n\n" + paragraph if current_chapter else paragraph
        
        if current_chapter.strip():
            chapters.append(current_chapter.strip())
        
        return chapters

def main():
    parser = argparse.ArgumentParser(description="Read2Me CLI - Generate audiobooks from text")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List voices command
    list_parser = subparsers.add_parser('list-voices', help='List available voices')
    
    # Generate single TTS
    tts_parser = subparsers.add_parser('tts', help='Generate single TTS audio')
    tts_parser.add_argument('text', help='Text to synthesize')
    tts_parser.add_argument('--voice', help='Built-in voice name')
    tts_parser.add_argument('--voice-file', help='Path to voice sample for cloning')
    tts_parser.add_argument('--output', help='Output file path')
    tts_parser.add_argument('--language', default='en', help='Language code (default: en)')
    
    # Process book command
    book_parser = subparsers.add_parser('book', help='Process book file into audiobook')
    book_parser.add_argument('input_file', help='Input text file (txt, epub, etc.)')
    book_parser.add_argument('--voice', help='Built-in voice name')
    book_parser.add_argument('--voice-file', help='Path to voice sample for cloning')
    book_parser.add_argument('--output-dir', help='Output directory for audiobook')
    book_parser.add_argument('--language', default='en', help='Language code (default: en)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = Read2MeCLI()
    
    if args.command == 'list-voices':
        cli.list_voices()
    
    elif args.command == 'tts':
        cli.generate_tts(
            text=args.text,
            voice=args.voice,
            voice_file=args.voice_file,
            output_file=args.output,
            language=args.language
        )
    
    elif args.command == 'book':
        cli.process_book(
            input_file=args.input_file,
            voice=args.voice,
            voice_file=args.voice_file,
            output_dir=args.output_dir,
            language=args.language
        )

if __name__ == "__main__":
    main()