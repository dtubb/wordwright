import re
import sys
from pathlib import Path

# File containing the list of adverbs
ADVERB_FILE = "adverbs.txt"

def load_adverbs():
    """Loads adverbs from a text file, ignoring comments and empty lines."""
    adverb_path = Path(ADVERB_FILE)

    if not adverb_path.exists():
        print(f"Error: {ADVERB_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    with open(adverb_path, "r", encoding="utf-8") as f:
        adverbs = [
            line.strip() for line in f 
            if line.strip() and not line.strip().startswith("#")
        ]

    return (r'\b(' + '|'.join(map(re.escape, adverbs)) + r')\b') if adverbs else None

def split_by_quotes(text):
    """Splits text into quoted and non-quoted sections."""
    pattern = re.compile(r'(["“])([^\1]*?)(["”])', re.MULTILINE)
    parts = []
    last_end = 0

    for match in pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            parts.append((False, text[last_end:start]))  # Non-quoted section
        parts.append((True, match.group(0)))  # Quoted section
        last_end = end

    if last_end < len(text):
        parts.append((False, text[last_end:]))  # Remaining non-quoted section

    return parts

# Load adverbs and construct the regex
ADVERB_REGEX = load_adverbs()
if ADVERB_REGEX:
    ADVERB_REGEX = re.compile(ADVERB_REGEX, re.MULTILINE)

# Improved QUOTE_REGEX to ensure proper quote handling
QUOTE_REGEX = r'(["“])([^\1]*?)(["”])'  # Match straight and curly double quotes

def remove_adverbs(text):
    parts = split_by_quotes(text)
    cleaned_parts = []

    for is_quoted, segment in parts:
        if not is_quoted and ADVERB_REGEX:
            segment = ADVERB_REGEX.sub('', segment)  # Remove adverbs
        cleaned_parts.append(segment)

    cleaned_text = ''.join(cleaned_parts)

    # Replace multiple spaces with a single space while preserving new lines
    cleaned_text = re.sub(r' {2,}', ' ', cleaned_text)

    return cleaned_text

def main():
    """Reads input from stdin, removes adverbs (outside quotes), and outputs the cleaned text."""
    if sys.stdin.isatty():
        print("Error: No input provided. Pipe text into this script.", file=sys.stderr)
        sys.exit(1)

    text = sys.stdin.read()
    cleaned_text = remove_adverbs(text)
    print(cleaned_text)

if __name__ == "__main__":
    main()