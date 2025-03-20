import re
import sys
import pyperclip
from pathlib import Path

PHRASES_FILE = "redundant_phrases.txt"

def load_replacement_phrases():
    """Loads the phrase replacements from the file."""
    phrase_dict = {}
    phrases_path = Path(PHRASES_FILE)

    if not phrases_path.exists():
        print(f"Error: {PHRASES_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    with open(PHRASES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("::")
            if len(parts) == 2:
                bad_phrase, replacement = parts[0].strip(), parts[1].strip()
                phrase_dict[bad_phrase] = replacement
            elif len(parts) == 1 and parts[0].strip():
                phrase_dict[parts[0].strip()] = ""

    return phrase_dict

def remove_phrases(text: str, phrase_dict: dict):
    """Removes or replaces redundant phrases in the text."""
    for bad_phrase, replacement in phrase_dict.items():
        pattern = rf"\b{re.escape(bad_phrase)}\b"
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def main():
    """Reads input, processes it, and prints or copies cleaned text."""
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        text = pyperclip.paste()

    phrase_dict = load_replacement_phrases()
    cleaned_text = remove_phrases(text, phrase_dict)

    if sys.stdin.isatty():
        pyperclip.copy(cleaned_text)
        print("Processed text copied to clipboard!")
    else:
        print(cleaned_text)

if __name__ == "__main__":
    main()