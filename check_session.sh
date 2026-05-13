#!/bin/bash

OBSIDIAN="$HOME/Documents/coin_tracker_interface"

echo "=== Git status ==="
git status --short

if [ -z "$(git status --short)" ]; then
  echo "✅ Nothing to commit"
else
  echo "⚠️  Uncommitted changes exist"
fi

echo ""
echo "=== Obsidian files (last modified) ==="
ls -la "$OBSIDIAN/current_state.md"
ls -la "$OBSIDIAN/current_task.md"