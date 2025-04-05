# WordWright

WordWright is a word processing pipeline that automates the editing steps I use daily. It processes standard input through various scripts to handle different editing tasks. Writing involves editing and revising, and making the text your own requires effort. Clichés, adverbs, and basic grammar fixes are useful early steps, and WordWright automates this process. It leverages OpenAI's language model to correct spelling, grammar, and punctuation errors, and improve formatting and style. Additionally, it uses DeepL's rewrite engine to clarify text.

When writing a book, I find myself editing or revising sections frequently. In the rush of writing ideas, I tend to make an large number of typos. During the writing of my first few books, I spent considerable time correcting these errors. Perhaps. ealrier generatiosn would have had tpyists, seceretaties, adn copy editors. But, as s tudent, I never did. So, I would often do a first round of editing uysing spell checkers and grammar checkers. Years ago,  for example, I created a simple screen macro that simply accepted the first suggestion in Word's spelling window. It wasn't alwaus right. but, more often or nto it was close enough. 

WordWright adopts a similar concept, but first it uses various scripts to remove adverbs and clichés, and then it uses  OpenAI and DeepL to fix grammar and revise the text lightly. I discuss this process on my [blog](https://www.tubb.ca/2023/06/writing-diary-9-on-a-morning-draft/))

I rely on this tool because I am not a good typist, making it my initial step in editing and the first step after making changes. However, I continue to revise the text multiple times afterward. It's a early editing tool, but it also risk losing a voice. So, I find it only reaslly useful early on in a writing profess. 

## Features

WordWright processes text in scripts:

1. Inspired by Roy Peter Clark's "How to Write Short," it removes redundant phrases using a predefined dictionary of common expressions with more concise alternatives, without changing text in quotes.
   - Example: Replaces "in order to" with "to" but leaves "He said, 'in order to succeed...'" unchanged.
2. It removes adverbs from the text, without changing text in quotes, because my writing style systematically includes adverbs. I might add them back later, but removing them is the first step.
   - Example: Removes "quickly" from "She quickly ran" but leaves "He said, 'She quickly ran...'" unchanged.
3. It asks a LLM (language model) to process the text to correct spelling, grammar, and punctuation errors, and improve formatting and style.
   - Example: Corrects "teh" to "the" and improves sentence structure.
4. It calls DeepL's rewrite engine to clarify the text. This one is a step to be used carefully, as sometimes it's helpful, and sometimes it's wrong. But, generally, I find it a very useful first editor.
   - Example: Rephrases "The quick brown fox jumps over the lazy dog" to "The fast brown fox leaps over the lazy dog."
5. It does a final cleanup to normalize punctuation, spacing, and formatting.
   - Example: Ensures consistent use of em dashes and removes extra spaces.

## Installation
To set up WordWright, follow these steps for a Mac. First, clone the WordWright repository from GitHub to your local machine. Next, set up a Conda environment specifically for WordWright to ensure that dependencies are managed and that the correct version of Python is installed. After setting up the environment, install all the required packages listed in the requirements.txt file, including essential libraries like typer, deepl, requests, and pyperclip. Additionally, you can use Keyboard Maestro to automate some of these setup steps for convenience. A sample Keyboard Maestro script is provided below to help automate the setup process. Finally, set up environment variables by obtaining API keys from OpenAI and DeepL, which are necessary for WordWright to function. These keys can be set up either temporarily for the current session or permanently by adding them to your shell configuration. 


### 1. Clone the Repository
```bash
git clone https://github.com/dtubb/wordwright.git
cd wordwright
```

### 2. Set Up Conda Environment

First, install Miniconda if you don't have it:
```bash
# Download Miniconda installer
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
# Install Miniconda
bash Miniconda3-latest-MacOSX-arm64.sh
# Follow the prompts, then restart your terminal
```

Create and activate the WordWright environment:
```bash
# Create a new conda environment with Python 3.11
conda create -n wordwright_env python=3.11

# Activate the environment
conda activate wordwright_env

# Verify Python version
python --version  # Should show Python 3.11.x
```

### 3. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installations
pip list | grep -E "typer|deepl|requests|pyperclip"
```

### 4. Set Up Environment Variables

WordWright needs two API keys to function. You can obtain these keys online:

- **OpenAI API Key**: Sign up at [OpenAI](https://www.openai.com/) and generate an API key from your account dashboard.
- **DeepL API Key**: Sign up at [DeepL](https://www.deepl.com/pro) and generate an API key from your account settings.

You can set these up in two ways:

#### Option 1: Temporary (for current session)

#### Option 2: Permanent (add to shell configuration)
```bash
# Add to your ~/.zshrc or ~/.bashrc
echo 'export OPENAI_API_KEY="your-openai-key-here"' >> ~/.zshrc
echo 'export DEEPL_API_KEY="your-deepl-key-here"' >> ~/.zshrc

# Reload your shell configuration
source ~/.zshrc
```

Verify the environment variables are set:
```bash
echo $OPENAI_API_KEY  # Should show your key
echo $DEEPL_API_KEY   # Should show your key
```

### 5. For macOS Users: Add zzh to PATH
```bash
# Add zzh to your shell configuration
echo 'export PATH="/usr/local/opt/zzh/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify zzh is in PATH
which zzh
```

## Usage

WordWright processes text in two ways:

1. Pipe text directly into the script:
```bash
cat your_text.txt | python wordwright.py
```

2. Process a specific file:
```bash
python wordwright.py your_text.txt
```
The processed text is output to stdout.

## Keyboard Maestro Integration

For Mac OS users, the project includes a Keyboard Maestro macro that uses Command-Option-C. This macro processes selected text through WordWright and puts it on the System Clipboard. It also opens BBEdit with a DIFF command on both texts.

To set up the Keyboard Maestro macro, use the one in the GitHub repository, or install it this way. The BBEdit diff code is optional. Set the full path of your user directory, rather than dtubb.

1. Open Keyboard Maestro
2. Create a new macro
3. Set the trigger to Command-Option-C
4. Add a "Execute Shell Script" action
5. Copy and paste the following script, adjusting the paths to match your system:

```bash
#!/bin/zsh
source /Users/dtubb/.zshrc
export PATH="/Users/dtubb/miniforge3/bin:/Applications/BBEdit.app/Contents/Helpers:$PATH"
source /Users/dtubb/miniforge3/etc/profile.d/conda.sh
conda activate wordwright_env

cd /Users/dtubb/code/wordwright

pbpaste > /tmp/before.txt

python /Users/dtubb/code/wordwright/wordwright.py < /tmp/before.txt | tee /tmp/after.txt | pbcopy

/Applications/BBEdit.app/Contents/Helpers/bbdiff /tmp/before.txt /tmp/after.txt || echo "bbdiff failed" >> /tmp/km_error.log
```

Make sure to:
- Update the paths to match your system
- Ensure BBEdit is installed, or comment out the last line.
- Have the conda environment activated
- Have the required API keys set in your environment

## Project Structure

- `wordwright.py`: Main script that orchestrates the text processing pipeline

- `remove_adverbs.py`: Removes adverbs while preserving quoted content
- `adverbs.txt`: Dictionary of adverbs to remove

- `remove_phrases.py`: Removes redundant phrases using predefined replacements
- `redundant_phrases.txt`: Dictionary of redundant phrases and their replacements

- `llm_cleanup.py`: Processes text through an LLM for grammar and style improvements
- `deepl_write.py`: Enhances text using DeepL's rephrasing engine

- `final_cleanup.py`: Performs final text normalization and formatting

## Dependencies

WordWright requires the following Python packages with exact versions:
- typer==0.9.4: For command-line interface
- deepl==1.21.1: For text rephrasing
- requests==2.32.3: For API calls
- pyperclip==1.8.2: For clipboard operations

## License

MIT License

## Citation

If you use WordWright in your work, please cite it as:

Tubb, Daniel. (2025). WordWright: A Text Processing Pipeline for Writing [Computer software]. Retrieved from https://github.com/dtubb/wordwright