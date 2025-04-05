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
    # Find all quoted text in the input and store them
    quoted_matches = re.findall(r'(["\'].*?["\'])', text)
    # Replace quoted text with a placeholder to process non-quoted text
    placeholder_text = re.sub(r'(["\'].*?["\'])', "QUOTE_PLACEHOLDER", text)

    # Process the text outside of quotes by removing adverbs and redundant phrases
    processed_text = remove_adverbs(remove_phrases(placeholder_text))

    # Restore the original quoted text back into the processed text
    for match in quoted_matches:
        processed_text = processed_text.replace("QUOTE_PLACEHOLDER", match, 1)

    return processed_text

# Read input text from standard input
input_text = sys.stdin.read().strip()

# Process the input text, preserving quoted sections
processed_text = preserve_quotes_and_process(input_text)

# Use DeepL to rephrase the processed text, targeting US English
result = deepl_client.rephrase_text(processed_text, target_lang="EN-US")

# Output the rephrased text to standard output
print(result.text)