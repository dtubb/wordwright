# WordWright Repository

## Folder Structure
```
WordWright/
│-- wordwright.py          # Main script
│-- README.md              # Project overview
│-- requirements.txt       # Dependencies
│-- .gitignore             # Ignore unnecessary files
│-- LICENSE                # License (MIT by default)
│-- macros/                # Folder for Keyboard Maestro macros
│   └── keyboard_macro.kmmacros
```

### 1. `README.md`
```markdown
# WordWright

**Automated text refinement with craft—turning rough drafts into polished prose.**

WordWright is a text automation tool designed to streamline the editing process by:
- Converting clipboard text to Markdown
- Removing adverbs and filler words
- Stripping unnecessary phrases
- Running text through an LLM for refinement
- Cleaning up extraneous characters
- Formatting hyphens properly

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python wordwright.py
```

For automation, use **Keyboard Maestro** to trigger this script via clipboard or file input.

## License
MIT License
```

### 2. `wordwright.py`
```python
import pyperclip
import re
import openai

# Load clipboard text
text = pyperclip.paste()

# Convert to Markdown
text = re.sub(r'\n{2,}', '\n\n', text.strip())

# Remove adverbs (simplified example)
adverbs = ["really", "very", "basically", "actually", "literally"]
for adverb in adverbs:
    text = re.sub(rf'\b{adverb}\b', '', text, flags=re.IGNORECASE)

# Run through LLM for refinement
openai.api_key = "your-api-key-here"
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"Refine this text concisely: {text}"}]
)
text = response["choices"][0]["message"]["content"]

# Clean extraneous characters and fix hyphens
text = re.sub(r'\s+[–—-]\s+', ' - ', text)  # Normalize dashes
text = re.sub(r'“|”', '"', text)  # Standardize quotes
text = re.sub(r'‘|’', "'", text)  # Standardize apostrophes

# Copy back to clipboard
pyperclip.copy(text)
print("Processed text copied to clipboard!")
```

### 3. `.gitignore`
```gitignore
__pycache__/
*.pyc
*.pyo
.env
*.kmmacros
```

### 4. `LICENSE`
```plaintext
MIT License

Copyright (c) 2025

Permission is hereby granted...
```

### 5. `requirements.txt`
```plaintext
pyperclip
openai
```

### 6. Keyboard Maestro Macro (`macros/keyboard_macro.kmmacros`)
This will need to be created in **Keyboard Maestro** manually but should:
- Trigger `wordwright.py` from clipboard input.
- Save the processed text back to the clipboard.

Let me know if you want a more refined version!
