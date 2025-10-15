"""
Read2Me - Simple audiobook generation toolkit
"""

from .lib.read2me_lib import AudiobookGenerator, quick_tts, book_to_audio
from .api.bookshelf_integration import BookshelfConnector

__version__ = "1.0.0"
__all__ = ["AudiobookGenerator", "quick_tts", "book_to_audio", "BookshelfConnector"]