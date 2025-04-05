import sys
import re

def simple_cleanup(text):
    # Replace straight double quotes with smart quotes
    text = re.sub(r'"(.*?)"', r'“\1”', text)

    # Replace straight single quotes/apostrophes with smart ones
    # The first regex handles quotes not surrounded by word characters
    text = re.sub(r"(?<!\w)'(.*?)'(?!\w)", r'‘\1’', text)
    # The second regex handles contractions and possessives
    text = re.sub(r"(\w)'(\w)", r"\1’\2", text)

    # Replace triple dots or spaced ellipses with a single ellipsis character
    text = re.sub(r"\.\s?\.\s?\.", "…", text)

    # Replace different dash patterns with appropriate dashes
    # Triple dash to em dash
    text = re.sub(r" ?- ?- ?- ?", "—", text)
    # Double dash to en dash
    text = re.sub(r" ?-- ?", "–", text)
    # Single dash to em dash, but only if not surrounded by word characters
    text = re.sub(r"(?<!\w) ?- ?(?!\w)", "—", text)

    # Remove any space before punctuation marks
    text = re.sub(r" (\.|,|!|\?|:|;)", r"\1", text)

    # Remove double spaces and replace them with a single space
    text = re.sub(r" {2,}", " ", text)

    # Remove space after punctuation at the end of a paragraph
    text = re.sub(r"([.!?])\s+\n", r"\1\n", text)

    # Normalize line endings to Unix style
    text = text.replace('\r\n', '\n')

    # Normalize various Unicode whitespace characters to a standard space
    text = re.sub(r'[\u00A0\u2002\u2003\u2009]', ' ', text)

    # Normalize hyphen spacing by removing spaces around hyphens
    text = re.sub(r"\s*-\s*", "-", text)

    # Collapse three or more newlines into just two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces between multiple punctuation marks
    text = re.sub(r'([?!.,])\s+([?!.,])', r'\1\2', text)

    # Strip leading and trailing whitespace from each line
    text = '\n'.join(line.strip() for line in text.splitlines())

    return text

if __name__ == "__main__":
    # Read input text from standard input
    input_text = sys.stdin.read()
    
    # Apply the simple_cleanup function to the input text
    output_text = simple_cleanup(input_text)
    
    # Write the cleaned text to standard output
    sys.stdout.write(output_text)
