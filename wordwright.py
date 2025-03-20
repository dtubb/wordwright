import typer
import pyperclip
import sys
import re
import subprocess
from pathlib import Path

app = typer.Typer()

def read_input(input_source: str = None):
    """Reads input from stdin, a file, or clipboard."""
    if input_source:
        file_path = Path(input_source)
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")
        else:
            typer.echo(f"Error: File '{input_source}' not found.", err=True)
            raise typer.Exit(1)
    elif not sys.stdin.isatty():
        return sys.stdin.read()
    else:
        return pyperclip.paste()

def convert_to_markdown(text: str):
    """Converts text to Markdown format."""
    return re.sub(r'\n{2,}', '\n\n', text.strip())

def remove_adverbs(text: str):
    """Calls the remove_adverbs.py script and processes text."""
    result = subprocess.run(
        ["python", "remove_adverbs.py"], input=text, text=True, capture_output=True
    )
    return result.stdout.strip()

def remove_phrases(text: str):
    """Calls the remove_phrases.py script and processes text."""
    result = subprocess.run(
        ["python", "remove_phrases.py"], input=text, text=True, capture_output=True
    )
    return result.stdout.strip()

@app.command()
def main(input_source: str = None):
    """Process input text, convert it to Markdown, remove adverbs, and remove redundant phrases."""
    text = read_input(input_source)
    markdown_text = convert_to_markdown(text)
    cleaned_text = remove_adverbs(markdown_text)
    final_text = remove_phrases(cleaned_text)
    typer.echo(final_text)

if __name__ == "__main__":
    app()