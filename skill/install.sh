#!/usr/bin/env bash
# Install the readout-lens skill as a symlink (per-project by default, --global for ~/.claude).
set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_DIR/skill/readout-lens"
if [[ "${1:-}" == "--global" ]]; then
  DEST="$HOME/.claude/skills/readout-lens"
else
  DEST="$(pwd)/.claude/skills/readout-lens"
fi
mkdir -p "$(dirname "$DEST")"
ln -sfn "$SRC" "$DEST"
echo "installed: $DEST -> $SRC"
echo "verify   : cd $REPO_DIR && python3 -m pytest -q"
