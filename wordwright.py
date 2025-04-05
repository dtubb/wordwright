import typer
import sys
import subprocess
from pathlib import Path

# Initialize a Typer application
app = typer.Typer()

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

def run_script(script_name: str, text: str):
    """Runs an external script with text input via stdin and returns its stdout output.
    
    This function uses subprocess to execute another Python script, passing the text
    as input. If the script execution fails (non-zero exit code), it raises an error and exits.
    """
    result = subprocess.run(
        ["python", script_name],
        input=text,
        text=True,
        capture_output=True
    )
    if result.returncode != 0:
        typer.echo(f"Error running {script_name}: {result.stderr}", err=True)
        raise typer.Exit(1)
    return result.stdout.strip()

def run_deepl(text: str):
    """Runs the DeepL processing script.
    
    This function is a specific use case of run_script, tailored to execute the
    'deepl_write.py' script, which is assumed to perform some form of text processing.
    """
    return run_script("deepl_write.py", text)

@app.command()
def main(input_source: str = None):
    """Main command for processing input text.
    
    This function orchestrates the text processing pipeline:
    1. Reads input from a file or stdin.
    2. Sequentially processes the text through various scripts:
       - Removes redundant phrases.
       - Removes adverbs.
       - Cleans up using a language model (LLM).
       - Processes with DeepL for further refinement.
       - Final cleanup for normalization.
    3. Outputs the final processed text.
    """
    text = read_input(input_source)
    
    # Remove redundant phrases from the text
    phrases_text = run_script("remove_phrases.py", text)
    
    # Remove adverbs from the text
    adverbs_text = run_script("remove_adverbs.py", phrases_text)
           
    # Clean up the text using a language model
    llm_text = run_script("llm_cleanup.py", adverbs_text)
    
    # Process the text with DeepL for further refinement
    deepl_text = run_deepl(llm_text)

    # Perform final cleanup and normalization
    final_text = run_script("final_cleanup.py", deepl_text)
    
    # Output the final processed text
    typer.echo(final_text)

if __name__ == "__main__":
    app()