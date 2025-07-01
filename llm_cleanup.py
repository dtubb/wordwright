import argparse
import os
import requests
import time
import re
import sys

def read_input(file_path):
    # If file_path is "-" or not provided, read from standard input
    if file_path == "-" or file_path is None:
        return sys.stdin.read()
    else:
        # Read from the specified file path
        with open(file_path, 'r') as file:
            return file.read()

def chunk_text(text, max_words=1000):
    """Split text into chunks of approximately max_words words, respecting paragraph boundaries."""
    # Split into paragraphs while preserving empty lines
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for line in lines:
        # Count words in current line (if it's not empty)
        line_word_count = len(line.split()) if line.strip() else 0
        
        # If adding this line would exceed max_words and we have content, start a new chunk
        if current_word_count + line_word_count > max_words and current_chunk and line.strip():
            # Join current chunk and add to chunks list
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_word_count = 0
        
        # Add line to current chunk
        current_chunk.append(line)
        current_word_count += line_word_count
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

def send_to_llm(chunk, api_key, model="gpt-4.1-mini"):
    # Define the prompt for the language model
    prompt = f'''Imagine yourself as an AI copy editor, proofreader, and first reader. I will provide you with text enclosed in double quotation marks. Without making substantive changes, your task is to:

- Convert written out punctation, new paragraph, etc. into actual punctation, new paragraphs, etc. replace them, with the , the . and the new lines.
- Fix any spelling, grammar, and punctuation errors.
- PRESERVE the original paragraph structure and spacing - do not merge paragraphs together.
- If making minor edits like adding a word, put the changes in [square brackets].
- Flag any awkward phrases, repeated words, or errors using double curly braces {{}}. Please include what each checkmark flags to provide specific feedback directly inside the curly brace {{}}.
- Add any bold/italic formatting needed.
- Revise ALL CAPS to sentence case or lower case as apropriate.
- Remove {{del}} and fix extra spaces.
- DO NOT CHANGE QUOTATIONS.
- DO NOT ADD QUOTES AROUND MARKDOWN HEADINGS (lines starting with #).
- PRESERVE ALL MARKDOWN HEADINGS EXACTLY AS THEY ARE (e.g., "# 001. Title" should remain "# 001. Title").
- Rewrite passive to active voice.
- RETURN ONLY CORRECTED TEXT. DO NOT LIST CHANGES.
– Replace dashes between words with a "---" or "--" for EM and EN dashes. With spaces. e.g. " — " or " – ".

"{chunk}"'''
    if model == "gpt-3.5-turbo":
        # Send a request to the GPT-3.5-turbo model using OpenAI's chat completions endpoint
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",  # Use the provided API key for authorization
                "Content-Type": "application/json"  # Specify the content type as JSON
            },
            json={
                "model": "gpt-3.5-turbo",  # Specify the model to use
                "messages": [
                    {"role": "system", "content": "You are a copy editor. PRESERVE the exact paragraph structure, spacing, and line breaks of the input text. Do not merge paragraphs or change the formatting."},
                    {"role": "user", "content": prompt}
                ],  # Send the prompt as a user message
                "max_tokens": 1500  # Limit the response to 1500 tokens
            }
        )
        response.raise_for_status()  # Raise an error if the response status is not successful
        return response.json()['choices'][0]['message']['content']  # Extract and return the content from the response
    elif model == "gpt-4":
        # Send a request to the GPT-4 model using OpenAI's chat completions endpoint
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are a copy editor. PRESERVE the exact paragraph structure, spacing, and line breaks of the input text. Do not merge paragraphs or change the formatting."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1500
            }
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    elif model == "gpt-4.1-mini":
        # Send a request to the GPT-4.1-mini model using OpenAI's chat completions endpoint
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4.1-mini",
                "messages": [
                    {"role": "system", "content": "You are a copy editor. PRESERVE the exact paragraph structure, spacing, and line breaks of the input text. Do not merge paragraphs or change the formatting."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1500
            }
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    else:
        # Raise an error if the specified model is not supported
        raise NotImplementedError("Only gpt-3.5-turbo, gpt-4, and gpt-4.1-mini models are implemented.")
    
def cleanup_text(file_path, api_key, model="gpt-3.5-turbo"):
    # Read the input text
    text = read_input(file_path)
    
    # Get the original spacing pattern from environment variable
    original_spacing = os.environ.get('ORIGINAL_SPACING', 'none')
    
    # Split the text into manageable chunks
    chunks = chunk_text(text)
    cleaned_text = []

    for chunk in chunks:
        for attempt in range(3):  # Retry up to 3 times
            try:
                # Send the chunk to the language model for processing
                response = send_to_llm(chunk, api_key, model)
                cleaned_text.append(response.strip())  # Strip whitespace from the response
                break  # Exit retry loop on success
            except requests.exceptions.HTTPError as e:
                # Handle HTTP errors, specifically rate limiting
                if e.response is not None and e.response.status_code == 429:
                    wait_time = 2 * (2 ** attempt)  # Exponential backoff: 2, 4, 8 seconds
                    print(f"Rate limited (429). Error: {e}. Retrying in {wait_time} seconds...")
                else:
                    wait_time = 2
                    print(f"HTTP error: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            except Exception as e:
                # Handle any other exceptions
                wait_time = 2
                print(f"Error: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        else:
            # Log failure after 3 attempts
            print("Failed to process chunk after 3 attempts.")

    # Join cleaned chunks into a single string
    if original_spacing == 'double':
        # Preserve double newlines between chunks
        final_output = "\n\n".join(cleaned_text)
    elif original_spacing == 'single':
        # Preserve single newlines between chunks
        final_output = "\n".join(cleaned_text)
    else:  # 'none'
        # Join with single newlines
        final_output = "\n".join(cleaned_text)

    # Remove surrounding triple backticks if present
    final_output = re.sub(r"^```(?:markdown)?\n?", "", final_output)
    final_output = re.sub(r"\n?```$", "", final_output)
    
    # Remove surrounding quotation marks that LLM might add
    final_output = re.sub(r'^["""\']+', '', final_output)
    final_output = re.sub(r'["""\']+$', '', final_output)
    
    # Pre-process: Separate headings from text that are on the same line
    # Pattern: # Heading Text -> # Heading\nText
    # More precise pattern that handles periods and doesn't split headings incorrectly
    # DISABLED: This was mangling headings incorrectly
    # final_output = re.sub(r'(# \d+\.\s*[^\n]+?)(\s+[A-Z][^\n]*)', r'\1\n\2', final_output)

    # Handle paragraph spacing based on original pattern
    if original_spacing == 'double':
        # Keep double newlines between paragraphs - preserve the structure as is
        final_output = final_output
    elif original_spacing == 'single':
        # Keep single newlines between paragraphs
        final_output = final_output
    else:  # 'none'
        # Keep no newlines between paragraphs, but ensure headings are followed by newlines
        result_lines = []
        for i, line in enumerate(final_output.split('\n')):
            result_lines.append(line)
            # If this line is a heading and not the last one, add a newline
            if line.strip().startswith('#') and i < len(final_output.split('\n')) - 1:
                result_lines.append('')  # Add empty line after heading
        # Join with newlines instead of spaces to preserve the empty lines
        final_output = '\n'.join(result_lines)

    return final_output

def main():
    # Set up argument parser for command line inputs
    parser = argparse.ArgumentParser(description="Clean up text using an LLM.")
    parser.add_argument("file", nargs="?", default="-", help="Path to the input text file, or '-' to read from standard input.")
    parser.add_argument("--api_key", default=None, help="API key for OpenAI or LM Studio. If not provided, will attempt to load from environment variable OPENAI_API_KEY.")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="Model to use (default: gpt-3.5-turbo).")
    
    args = parser.parse_args()
    
    # Retrieve API key from arguments or environment variable
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("API key not provided and not found in environment variable OPENAI_API_KEY.")
        return

    # Clean up the text using the specified model
    cleaned_text = cleanup_text(args.file, api_key, args.model)
    print(cleaned_text)

if __name__ == "__main__":
    main()