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

# Read input text from standard input
input_text = sys.stdin.read().strip()

# Process the input text, preserving quoted sections
processed_text = preserve_quotes_and_process(input_text)

# Use DeepL to rephrase the processed text, targeting US English
result = deepl_client.rephrase_text(processed_text, target_lang="EN-US")

# Handle paragraph spacing in the DeepL result
lines = [line.strip() for line in result.text.split('\n') if line.strip()]
original_spacing = os.environ.get('ORIGINAL_SPACING', 'none')

if original_spacing == 'double':
    # Keep double newlines between paragraphs
    result_text = '\n\n'.join(lines)
elif original_spacing == 'single':
    # Keep single newlines between paragraphs
    result_text = '\n'.join(lines)
else:  # 'none'
    # Keep no newlines between paragraphs
    result_text = ' '.join(lines)

# Output the rephrased text to standard output
print(result_text)