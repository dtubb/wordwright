import re
import sys
from pathlib import Path

# File containing the list of adverbs
ADVERB_FILE = "adverbs.txt"

def load_adverbs():
    """Loads adverbs from a text file, ignoring comments and empty lines."""
    adverb_path = Path(ADVERB_FILE)

    # Check if the adverb file exists
    if not adverb_path.exists():
        print(f"Error: {ADVERB_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    # Read adverbs from the file, ignoring comments and empty lines
    with open(adverb_path, "r", encoding="utf-8") as f:
        adverbs = [
            line.strip() for line in f 
            if line.strip() and not line.strip().startswith("#")
        ]

    # Construct a regex pattern to match any of the adverbs as whole words.
    # The pattern is built by joining all adverbs with the '|' (OR) operator,
    # ensuring each adverb is treated as a whole word using the word boundary '\b'.
    # The 're.escape' function is used to escape any special characters in the adverbs.
    # If the adverbs list is empty, return None.
    return (r'\b(' + '|'.join(map(re.escape, adverbs)) + r')\b') if adverbs else None

def split_by_quotes(text):
    """
    Splits text into quoted and non-quoted sections.

    This function will look for quoted sections in the text using a regex pattern
    that matches both straight and curly double quotes. It will then split the text
    into parts, marking each part as either quoted or non-quoted.

    The resulting list of parts will contain tuples where the first element is a boolean
    indicating whether the part is quoted (True) or not (False), and the second element
    is the actual text of that part.
    """
    # Compile a regex pattern to match quoted sections
    pattern = re.compile(r'(["“])([^\1]*?)(["”])', re.MULTILINE)
    parts = []
    last_end = 0

    # Iterate over all matches of quoted sections
    for match in pattern.finditer(text):
        start, end = match.span()
        # Add non-quoted section before the quoted section
        if start > last_end:
            parts.append((False, text[last_end:start]))  # Non-quoted section
        # Add the quoted section
        parts.append((True, match.group(0)))  # Quoted section
        last_end = end

    # Add any remaining non-quoted section after the last quoted section
    if last_end < len(text):
        parts.append((False, text[last_end:]))  # Remaining non-quoted section

    return parts

# Load adverbs and construct the regex
ADVERB_REGEX = load_adverbs()
if ADVERB_REGEX:
    # Compile the regex pattern for adverbs
    ADVERB_REGEX = re.compile(ADVERB_REGEX, re.MULTILINE)

# Improved QUOTE_REGEX to ensure proper quote handling
QUOTE_REGEX = r'(["“])([^\1]*?)(["”])'  # Match straight and curly double quotes

def remove_adverbs(text):
    # Split the text into quoted and non-quoted parts
    parts = split_by_quotes(text)
    cleaned_parts = []

    # Process each part separately
    for is_quoted, segment in parts:
        # Remove adverbs only from non-quoted sections
        if not is_quoted and ADVERB_REGEX:
            segment = ADVERB_REGEX.sub('', segment)  # Remove adverbs
        cleaned_parts.append(segment)

    # Combine all parts back into a single text
    cleaned_text = ''.join(cleaned_parts)

    # Replace multiple spaces with a single space while preserving new lines
    cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)

    return cleaned_text

def main():
    """Reads input from stdin, removes adverbs (outside quotes), and outputs the cleaned text."""

    # Check if input is provided via stdin
    if sys.stdin.isatty():
        print("Error: No input provided. Pipe text into this script.", file=sys.stderr)
        sys.exit(1)

    # Read the input text
    text = sys.stdin.read()

    # Remove adverbs from the text
    cleaned_text = remove_adverbs(text)
    
    # Output the cleaned text
    print(cleaned_text)

if __name__ == "__main__":
    main()