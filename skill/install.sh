#!/usr/bin/env bash
# Install the readout-lens skill as a symlink (per-project by default, --global for ~/.claude).
# PRIVATE / PROPRIETARY (see repo LICENSE EXCEPTIONS) — do not publish.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_DIR/skill/readout-lens"
if [[ "${1:-}" == "--global" ]]; then
  DEST="$HOME/.claude/skills/readout-lens"
else
  DEST="$(pwd)/.claude/skills/readout-lens"
fi
mkdir -p "$(dirname "$DEST")"
if [[ -e "$DEST" && ! -L "$DEST" ]]; then
  echo "refusing to replace non-symlink at $DEST — remove it manually first" >&2
  exit 1
fi
ln -sfn "$SRC" "$DEST"
echo "installed: $DEST -> $SRC"
echo "verify   : cd $REPO_DIR && python3 -m pytest -q"
