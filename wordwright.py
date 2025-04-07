import typer
import sys
import subprocess
from pathlib import Path
import re
import os

# Initialize a Typer application
app = typer.Typer()

def detect_paragraph_spacing(text: str) -> str:
    """Detect the paragraph spacing pattern in the input text"""
    # Look for double newlines first (markdown style)
    if re.search(r'\n\s*\n', text):
        return 'double'  # Markdown style (double newlines)
    elif '\n' in text:
        return 'single'  # Word processor style (single newlines)
    else:
        return 'none'    # No newlines between paragraphs

def normalize_line_spacing(text: str, target_spacing: int) -> str:
    """Normalizes the line spacing in the text to the target number of newlines.
    
    Args:
        text: The input text
        target_spacing: The desired number of newlines between paragraphs (1 or 2)
    
    Returns:
        str: Text with normalized line spacing
    """
    if target_spacing == 2:
        # First, collapse any 3+ newlines to 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Then ensure paragraphs are separated by exactly two newlines
        text = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', text)
    else:
        # Ensure exactly one newline between paragraphs
        text = re.sub(r'\n{2,}', '\n', text)
    return text

def read_input(input_source: str = None):
    """Reads input from stdin or a file.
    
    If an input source is provided, it attempts to read from the specified file.
    If no input source is provided, it checks if input is being piped via stdin.
    If neither condition is met, it raises an error and exits.
    """
    if input_source:
        file_path = Path(input_source)
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        else:
            typer.echo(f"Error: File '{input_source}' not found.", err=True)
            raise typer.Exit(1)
    elif not sys.stdin.isatty():  # If input is being piped
        return sys.stdin.read()
    else:
        typer.echo("Error: No input provided. Pipe text into this script or specify a file.", err=True)
        raise typer.Exit(1)

def run_script(script_name: str, text: str, env_vars: dict = None):
    """Runs an external script with text input via stdin and returns its stdout output.
    
    This function uses subprocess to execute another Python script, passing the text
    as input. If the script execution fails (non-zero exit code), it raises an error and exits.
    """
    # Create environment with additional variables if provided
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    result = subprocess.run(
        ["python", script_name],
        input=text,
        text=True,
        capture_output=True,
        env=env
    )
    if result.returncode != 0:
        typer.echo(f"Error running {script_name}: {result.stderr}", err=True)
        raise typer.Exit(1)
    # Only strip trailing newlines, not leading ones
    return result.stdout.rstrip('\n')

def run_deepl(text: str, env_vars: dict = None):
    """Runs the DeepL processing script.
    
    This function is a specific use case of run_script, tailored to execute the
    'deepl_write.py' script, which is assumed to perform some form of text processing.
    """
    return run_script("deepl_write.py", text, env_vars)

@app.command()
def main(input_source: str = None):
    """Main command for processing input text.
    
    This function orchestrates the text processing pipeline:
    1. Reads input from a file or stdin.
    2. Detects the original line spacing pattern
    3. Sequentially processes the text through various scripts
    4. Restores the original line spacing pattern
    5. Outputs the final processed text.
    """
    text = read_input(input_source)
    
    # Detect the original paragraph spacing pattern
    original_spacing = detect_paragraph_spacing(text)
    
    # Create environment variables to pass spacing pattern
    env_vars = {'ORIGINAL_SPACING': original_spacing}
    
    # Remove redundant phrases from the text
    phrases_text = run_script("remove_phrases.py", text, env_vars)
    
    # Remove adverbs from the text
    adverbs_text = run_script("remove_adverbs.py", phrases_text, env_vars)
           
    # Clean up the text using a language model
    llm_text = run_script("llm_cleanup.py", adverbs_text, env_vars)
    
    # Process the text with DeepL for further refinement
    deepl_text = run_deepl(llm_text, env_vars)

    # Perform final cleanup and normalization
    final_text = run_script("final_cleanup.py", deepl_text, env_vars)
    
    # Output the final processed text
    typer.echo(final_text)

if __name__ == "__main__":
    app()