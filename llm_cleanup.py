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

def chunk_text(text, max_chunk_size=2000):
    # Split text into sentences using punctuation as delimiters
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # Check if adding the sentence exceeds the max chunk size
        if len(current_chunk) + len(sentence) + 1 > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk)  # Add the current chunk to the list
            current_chunk = sentence  # Start a new chunk with the current sentence
        else:
            if current_chunk:
                current_chunk += " " + sentence  # Append sentence to the current chunk
            else:
                current_chunk = sentence  # Initialize the current chunk with the sentence
    if current_chunk:
        chunks.append(current_chunk)  # Add the last chunk if it exists
    return chunks

def send_to_llm(chunk, api_key, model="openai"):
    # Define the prompt for the language model
    prompt = f'''Imagine yourself as an AI copy editor, proofreader, and first reader. I will provide you with text enclosed in double quotation marks. Without making substantive changes, your task is to:

- Convert written out punctation, new paragraph, etc. into actual punctation, new paragraphs, etc. replace them, with the , the . and the new lines.
- Fix any spelling, grammar, and punctuation errors.
- Break the text into paragraphs at logical places.
- If making minor edits like adding a word, put the changes in [square brackets].
- Flag any awkward phrases, repeated words, or errors using double curly braces {{}}. Please include what each checkmark flags to provide specific feedback directly inside the curly brace {{}}.
- Add any bold/italic formatting needed.
- Revise ALL CAPS to sentence case or lower case as apropriate.
- Remove {{del}} and fix extra spaces.
- DO NOT CHANGE QUOTATIONS.
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
                "model": "gpt-4o-mini-2024-07-18",  # Specify the model to use
                "messages": [{"role": "user", "content": prompt}],  # Send the prompt as a user message
                "max_tokens": 1500  # Limit the response to 1500 tokens
            }
        )
        response.raise_for_status()  # Raise an error if the response status is not successful
        return response.json()['choices'][0]['message']['content']  # Extract and return the content from the response
    elif model == "openai":
        # Send a request to the OpenAI davinci-codex model using the completions endpoint
        response = requests.post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            headers={"Authorization": f"Bearer {api_key}"},  # Use the provided API key for authorization
            json={"prompt": prompt, "max_tokens": 1500}  # Send the prompt and limit the response to 1500 tokens
        )
        response.raise_for_status()  # Raise an error if the response status is not successful
        return response.json()['choices'][0]['text']  # Extract and return the text from the response
    else:
        # Raise an error if the specified model is not supported
        raise NotImplementedError("Only gpt-3.5-turbo and OpenAI davinci-codex models are implemented.")
    
def cleanup_text(file_path, api_key, model="openai"):
    # Read the input text
    text = read_input(file_path)
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
    final_output = "\n".join(cleaned_text)

    # Remove surrounding triple backticks if present
    final_output = re.sub(r"^```(?:markdown)?\n?", "", final_output)
    final_output = re.sub(r"\n?```$", "", final_output)

    # Remove opening and closing quotation marks if present
    final_output = final_output.strip('"')

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