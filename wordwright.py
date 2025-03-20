import typer
import sys
import re
import subprocess
from pathlib import Path

app = typer.Typer()

def read_input(input_source: str = None):
    """Reads input from stdin or a file."""
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

def convert_to_markdown(text: str):
    """Converts text to Markdown format."""
    return re.sub(r'\n{2,}', '\n\n', text.strip())

def run_script(script_name: str, text: str):
    """Runs an external script with text input via stdin."""
    result = subprocess.run(
        ["python", script_name], input=text, text=True, capture_output=True
    )
    return result.stdout.strip()

@app.command()
def main(input_source: str = None):
    """Process input text, convert it to Markdown, remove adverbs, and remove redundant phrases."""
    text = read_input(input_source)
    markdown_text = convert_to_markdown(text)
    cleaned_text = run_script("remove_adverbs.py", markdown_text)
    final_text = run_script("remove_phrases.py", cleaned_text)
    typer.echo(final_text)

if __name__ == "__main__":
    app()