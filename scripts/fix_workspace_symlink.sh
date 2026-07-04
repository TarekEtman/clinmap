#!/usr/bin/env bash
set -euo pipefail
JOB="/Users/nati/Documents/JOB"
V1="$JOB/clinical-ai-eval-lab-v1"
LINK="$JOB/clinical-ai-eval-lab"

if [[ ! -d "$V1" ]]; then
  echo "Missing $V1"
  exit 1
fi

if [[ -e "$LINK" && ! -L "$LINK" ]]; then
  echo "ERROR: $LINK exists and is not a symlink. Rename or remove it manually."
  exit 1
fi

if [[ -L "$LINK" ]]; then
  echo "Symlink already exists:"
  ls -la "$LINK"
  exit 0
fi

ln -s clinical-ai-eval-lab-v1 "$LINK"
echo "Created: $LINK -> clinical-ai-eval-lab-v1"
ls -la "$LINK"
echo "Reopen Grok/Cursor workspace on $LINK or $V1 and start a new agent chat."