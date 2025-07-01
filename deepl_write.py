import os
import deepl
import re
import sys

from remove_adverbs import remove_adverbs
from remove_phrases import remove_phrases

# Load API key from environment variable
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

# Check if the API key is set, raise an error if not
if not DEEPL_API_KEY:
    raise ValueError("DEEPL_API_KEY is not set. Please export it in your environment.")

# Initialize DeepL Client with the API key
deepl_client = deepl.DeepLClient(DEEPL_API_KEY)

def preserve_quotes_and_process(text):
    # Get the original spacing pattern from environment variable
    original_spacing = os.environ.get('ORIGINAL_SPACING', 'none')
    
    # Find all quoted text in the input and store them
    quoted_matches = re.findall(r'([""].*?[""])', text)
    # Replace quoted text with a placeholder to process non-quoted text
    placeholder_text = re.sub(r'([""].*?[""])', "QUOTE_PLACEHOLDER", text)

    # Process the text outside of quotes by removing adverbs and redundant phrases
    processed_text = remove_adverbs(remove_phrases(placeholder_text))

    # Restore the original quoted text back into the processed text
    for match in quoted_matches:
        processed_text = processed_text.replace("QUOTE_PLACEHOLDER", match, 1)

    # Handle paragraph spacing based on original pattern
    lines = [line.strip() for line in processed_text.split('\n') if line.strip()]
    
    if original_spacing == 'double':
        # Keep double newlines between paragraphs
        processed_text = '\n\n'.join(lines)
    elif original_spacing == 'single':
        # Keep single newlines between paragraphs
        processed_text = '\n'.join(lines)
    else:  # 'none'
        # Keep no newlines between paragraphs
        processed_text = ' '.join(lines)

    return processed_text

def translate_text(text):
    # Split the text into quoted and non-quoted parts
    parts = split_by_quotes(text)
    translated_parts = []

    # Process each part separately
    for is_quoted, segment in parts:
        # Translate only non-quoted sections
        if not is_quoted:
            # Call DeepL API for translation
            translated_segment = deepl.translate(segment, target_lang='EN')
        else:
            translated_segment = segment
        translated_parts.append(translated_segment)

    # Combine all parts back into a single text
    translated_text = ''.join(translated_parts)

    return translated_text

def chunk_text(text, max_words=1000):
    """Split text into chunks of approximately max_words words, respecting paragraph boundaries."""
    # First split into paragraphs
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for paragraph in paragraphs:
        # Count words in current paragraph
        paragraph_word_count = len(paragraph.split())
        
        # If adding this paragraph would exceed max_words, start a new chunk
        if current_word_count + paragraph_word_count > max_words and current_chunk:
            # Join current chunk and add to chunks list
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_word_count = 0
        
        # Add paragraph to current chunk
        current_chunk.append(paragraph)
        current_word_count += paragraph_word_count
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def process_text_in_chunks(text):
    """Process text in chunks using DeepL, preserving paragraph structure and excluding headings."""
    # Get the original spacing pattern from environment variable
    original_spacing = os.environ.get('ORIGINAL_SPACING', 'none')
    
    # Split text into lines and process each non-heading line separately
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        if line.strip().startswith('#'):
            # Preserve headings exactly as they are
            processed_lines.append(line)
        elif line.strip():
            # Process non-empty, non-heading lines through DeepL
            try:
                result = deepl_client.rephrase_text(line.strip(), target_lang="EN-US")
                processed_lines.append(result.text)
            except Exception as e:
                # If DeepL fails, keep the original line
                print(f"DeepL processing failed for line: {e}", file=sys.stderr)
                processed_lines.append(line)
        else:
            # Preserve empty lines
            processed_lines.append(line)
    
    # Reconstruct the text with original spacing
    result_text = '\n'.join(processed_lines)
    
    return result_text

# Read input text from standard input
input_text = sys.stdin.read().strip()

# Process the input text, preserving quoted sections
processed_text = preserve_quotes_and_process(input_text)

# Process the text in chunks using DeepL
result_text = process_text_in_chunks(processed_text)

# Output the rephrased text to standard output
print(result_text)