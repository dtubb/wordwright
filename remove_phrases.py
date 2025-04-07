import re
import sys
import os

# 1) Load your phrase-replacements map (from redundant_phrases.txt)
PHRASE_MAP = {}
with open("redundant_phrases.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()  # Remove leading/trailing whitespace
        if not line or "::" not in line:  # Skip empty lines or lines without '::'
            continue
        phrase, replacement = line.split("::", 1)  # Split into phrase and replacement
        phrase = phrase.strip().lower()  # Normalize phrase to lowercase
        replacement = replacement.strip()  # Remove leading/trailing whitespace from replacement
        PHRASE_MAP[phrase] = replacement  # Add to the phrase map

# 2) Sort longer phrases first, so multi-word phrases match before single words
sorted_phrases = sorted(PHRASE_MAP.keys(), key=len, reverse=True)

# 3) Compile a regex that matches any of the keys as whole words, ignoring case
# Explanation:
# - \b: Word boundary to ensure we match whole words only.
# - ( ... ): Grouping for the alternation (|) of all phrases.
# - |: Alternation operator to match any one of the phrases.
# - re.escape: Escapes special characters in phrases to treat them as literals.
# - flags=re.IGNORECASE: Makes the regex case-insensitive.
PHRASE_REGEX = re.compile(
    r"\b(" + "|".join(map(re.escape, sorted_phrases)) + r")\b",
    flags=re.IGNORECASE
)

def phrase_replacement(match):
    """
    Called for every matched phrase. We strip punctuation, lowercase,
    and look up the correct replacement or an empty string.
    """
    matched_text = re.sub(r"[^\w\s]", "", match.group(1).strip().lower())
    return PHRASE_MAP.get(matched_text, "")

def remove_phrases(text):
    """
    Splits text into segments outside/inside quotes. Only the outside
    is subjected to phrase replacements, then normalizes spaces without
    destroying line breaks.
    """
    # Split on anything in quotes (straight or curly)
    segments = re.split(r'([\"“”].*?[\"“”])', text)

    processed_segments = []
    for segment in segments:
        # If segment looks quoted, leave it alone
        if segment.startswith('"') or segment.startswith('"'):
            processed_segments.append(segment)
        else:
            # Do phrase replacements in the non-quoted segment
            replaced_segment = PHRASE_REGEX.sub(phrase_replacement, segment)
            processed_segments.append(replaced_segment)

    combined_text = "".join(processed_segments)

    # Fix spacing before punctuation (, . ! ? etc.)
    combined_text = re.sub(r"\s+([.,;!?])", r"\1", combined_text)

    # Replace consecutive spaces (but preserve newlines!)
    # i.e. only shrink multiple spaces on the same line
    def shrink_spaces(line):
        return re.sub(r' {2,}', ' ', line)

    lines = combined_text.split('\n')
    lines = [shrink_spaces(line) for line in lines]
    cleaned_text = '\n'.join(lines)

    return cleaned_text

if __name__ == "__main__":
    # Read from stdin, apply replacements, print result
    text_in = sys.stdin.read()
    print(remove_phrases(text_in))