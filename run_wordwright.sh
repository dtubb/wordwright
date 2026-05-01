#!/bin/zsh
# WordWright launcher.
#
# Two modes:
#   1. Keyboard Maestro / hotkey (no args): edit the clipboard in place.
#      Original goes to /tmp/before.txt, edited to /tmp/after.txt and clipboard.
#   2. Automator / CLI (file path args): edit each file, write
#      <name>.edited.<ext> next to the source. Source is never overwritten.

set -euo pipefail

REPO="/Users/danieltubb/code/wordwright"
LOG="/tmp/wordwright.log"
echo "=== WordWright run: $(date) args=$# ===" >> "$LOG"

# Use absolute paths so Automator (which has no PATH) still finds tools.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# API keys.
[[ -f /Users/danieltubb/.config/wordwright/env.sh ]] && source /Users/danieltubb/.config/wordwright/env.sh

cd "$REPO"
PY="$REPO/.venv/bin/python"

if [[ $# -eq 0 ]]; then
    # Clipboard mode.
    echo "mode: clipboard" >> "$LOG"
    pbpaste > /tmp/before.txt
    "$PY" "$REPO/wordwright.py" < /tmp/before.txt | tee /tmp/after.txt | pbcopy
    echo "clipboard updated ($(wc -c < /tmp/after.txt) bytes)" >> "$LOG"
else
    # File mode.
    for src in "$@"; do
        echo "mode: file -- $src" >> "$LOG"
        if [[ ! -f "$src" ]]; then
            echo "ERROR: not a file: $src" | tee -a "$LOG" >&2
            continue
        fi
        dir="${src:h}"
        base="${src:t:r}"
        ext="${src:e}"
        out="$dir/$base.edited.${ext:-md}"
        "$PY" "$REPO/wordwright.py" "$src" > "$out"
        echo "wrote $out ($(wc -c < "$out") bytes)" >> "$LOG"
    done
fi

echo "=== done ===" >> "$LOG"
