import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_chapters(epub_path, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the EPUB file
    book = epub.read_epub(epub_path)

    chapter_count = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Parse HTML content
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # Extract text content
            text = soup.get_text()
            
            # Remove leading/trailing whitespace and extra newlines
            text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
            
            # Check if the content is not empty
            if text:
                chapter_count += 1
                output_file = os.path.join(output_dir, f"ch{chapter_count}.txt")
                
                # Write chapter content to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                print(f"Created {output_file}")

    print(f"Extracted {chapter_count} chapters.")

# Example usage
book_title = 'the_fountainhead'
epub_path = f'../data/epubs/{book_title}.epub'
output_dir = f'../data/split_books/{book_title}'
extract_chapters(epub_path, output_dir)