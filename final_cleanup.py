import sys
import re
import os

def detect_paragraph_spacing(text):
    """Detect the paragraph spacing pattern in the input text"""
    # Look for patterns of multiple newlines
    if re.search(r'\n{2,}', text):
        return 'double'  # Double or more newlines between paragraphs
    elif '\n' in text:
        return 'single'  # Single newlines between paragraphs
    else:
        return 'none'    # No newlines between paragraphs

def simple_cleanup(text, original_spacing='none'):
    """
    Clean up text while preserving the original paragraph spacing pattern.
    
    Args:
        text: The text to clean
        original_spacing: The original spacing pattern ('none', 'single', or 'double')
    """
    # First, normalize all line endings to Unix style
    text = text.replace('\r\n', '\n')
    
    # Split into paragraphs (non-empty lines)
    paragraphs = []
    current_paragraph = []
    
    for line in text.splitlines():
        line = line.strip()
        if line:
            current_paragraph.append(line)
        elif current_paragraph:  # Empty line and we have content
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
    
    # Don't forget the last paragraph
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    # Handle paragraph spacing based on original pattern
    if original_spacing == 'double':
        # Markdown style: double newlines between paragraphs
        text = '\n\n'.join(paragraphs)
    elif original_spacing == 'single':
        # Word processor style: single newlines between paragraphs
        text = '\n'.join(paragraphs)
    else:  # 'none'
        # No spacing between paragraphs
        text = ' '.join(paragraphs)

    # Handle double quotes (U+201C LEFT DOUBLE QUOTATION MARK, U+201D RIGHT DOUBLE QUOTATION MARK)
    text = re.sub(r'"([^"]*)"', '\u201c\\1\u201d', text)
    
    # Handle single quotes (U+2018 LEFT SINGLE QUOTATION MARK, U+2019 RIGHT SINGLE QUOTATION MARK)
    text = re.sub(r"'([^']*)'", '\u2018\\1\u2019', text)
    
    # Handle apostrophes in contractions and possessives (U+2019 RIGHT SINGLE QUOTATION MARK)
    text = re.sub(r"(\w)'(\w)", '\\1\u2019\\2', text)

    # Replace triple dots or spaced ellipses with a single ellipsis character
    text = re.sub(r"\.\s?\.\s?\.", "…", text)

    # Replace different dash patterns with appropriate dashes
    text = re.sub(r" ?- ?- ?- ?", "—", text)  # Triple dash to em dash
    text = re.sub(r" ?-- ?", "–", text)  # Double dash to en dash
    text = re.sub(r"(?<!\w) ?- ?(?!\w)", "—", text)  # Single dash to em dash
    text = re.sub(r" ?— ?", "—", text)  # Handle spaced em dashes

    # Remove any space before punctuation marks
    text = re.sub(r" (\.|,|!|\?|:|;)", r"\1", text)

    # Remove double spaces and replace them with a single space
    text = re.sub(r" {2,}", " ", text)

    return text

if __name__ == "__main__":
    # Read input text from standard input
    input_text = sys.stdin.read()
    
    # Get the original spacing pattern from command line argument or environment variable
    original_spacing = 'none'  # Default to no spacing
    if len(sys.argv) > 1:
        original_spacing = sys.argv[1]
    elif 'ORIGINAL_SPACING' in os.environ:
        original_spacing = os.environ['ORIGINAL_SPACING']
    
    # Apply the simple_cleanup function to the input text
    output_text = simple_cleanup(input_text, original_spacing)
    
    # Write the cleaned text to standard output
    sys.stdout.write(output_text)
