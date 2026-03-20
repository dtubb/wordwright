#!/bin/zsh
set -euo pipefail

# Activate the project's virtual environment
source /Users/dtubb/code/wordwright/.venv/bin/activate

# Ensure BBEdit helper tools are available
export PATH="/Applications/BBEdit.app/Contents/Helpers:$PATH"

# Load secrets if present
[[ -f /Users/dtubb/.config/wordwright/env.sh ]] && source /Users/dtubb/.config/wordwright/env.sh

cd /Users/dtubb/code/wordwright

pbpaste > /tmp/before.txt

python /Users/dtubb/code/wordwright/wordwright.py < /tmp/before.txt | tee /tmp/after.txt | pbcopy

# /Applications/BBEdit.app/Contents/Helpers/bbdiff /tmp/before.txt /tmp/after.txt || echo "bbdiff failed" >> /tmp/km_error.log 