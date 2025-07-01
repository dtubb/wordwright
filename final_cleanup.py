import sys
import re
import os
import smartypants

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
    
    # Remove surrounding quotation marks that LLM might add
    text = re.sub(r'^["""\']+', '', text)
    text = re.sub(r'["""\']+$', '', text)
    
    # Split the text into lines and process each line
    lines = text.splitlines()
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            # If this line starts with '#' (heading), preserve it exactly
            if line.startswith('#'):
                processed_lines.append(line)
            else:
                # Apply smartypants and other cleanup to non-heading lines
                processed_line = smartypants.smartypants(line, smartypants.Attr.u | smartypants.Attr.q | smartypants.Attr.b | smartypants.Attr.d | smartypants.Attr.e)
                
                # Replace triple dots or spaced ellipses with a single ellipsis character
                processed_line = re.sub(r"\.\s?\.\s?\.", "…", processed_line)
                
                # Replace different dash patterns with appropriate dashes
                processed_line = re.sub(r" ?- ?- ?- ?", "—", processed_line)  # Triple dash to em dash
                processed_line = re.sub(r" ?-- ?", "–", processed_line)  # Double dash to en dash
                processed_line = re.sub(r"(?<!\w) ?- ?(?!\w)", "—", processed_line)  # Single dash to em dash
                processed_line = re.sub(r" ?— ?", "—", processed_line)  # Handle spaced em dashes
                
                # Remove any space before punctuation marks
                processed_line = re.sub(r" (\.|,|!|\?|:|;)", r"\1", processed_line)
                
                # Remove double spaces and replace them with a single space
                processed_line = re.sub(r" {2,}", " ", processed_line)
                
                processed_lines.append(processed_line)
    
    # Handle paragraph spacing based on original pattern
    if original_spacing == 'double':
        # Markdown style: double newlines between paragraphs
        # Add empty lines between headings and content, and between content paragraphs
        result_lines = []
        for i, line in enumerate(processed_lines):
            result_lines.append(line)
            # If this line is a heading and not the last one, add an empty line
            if line.startswith('#') and i < len(processed_lines) - 1:
                result_lines.append('')
        text = '\n\n'.join(result_lines)
    elif original_spacing == 'single':
        # Word processor style: single newlines between paragraphs
        text = '\n'.join(processed_lines)
    else:  # 'none'
        # No spacing between paragraphs, but ensure headings are followed by newlines
        result_lines = []
        for i, line in enumerate(processed_lines):
            result_lines.append(line)
            # If this line is a heading and not the last one, add a newline
            if line.startswith('#') and i < len(processed_lines) - 1:
                result_lines.append('')  # Add empty line after heading
        # Join with newlines instead of spaces to preserve the empty lines
        text = '\n'.join(result_lines)

    # Normalize triple newlines to double newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

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
