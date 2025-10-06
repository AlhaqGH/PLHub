#!/usr/bin/env bash
# PLHub Launcher for Linux/macOS
# Makes PLHub commands short and language-independent
# Usage: plhub run, plhub build apk --release, etc.

# Get the directory where this script is located
PLHUB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Run PLHub with all arguments
python3 "$PLHUB_ROOT/plhub.py" "$@"
