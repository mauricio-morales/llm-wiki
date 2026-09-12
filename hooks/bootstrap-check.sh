#!/bin/bash
# SessionStart hook: orient a session opened on a wiki folder.
# Only ever prints a short pointer — setup itself is started explicitly, with /wiki-setup.
# Never fails the session: any error exits 0 with no output.

set -uo pipefail
DIR="${CLAUDE_PROJECT_DIR:-$PWD}"

if [ ! -f "$DIR/llm-wiki.yml" ]; then
  # Not a wiki folder (or not set up yet). Say nothing unless a wiki is clearly intended.
  if [ -d "$DIR/Wiki" ]; then
    echo "LLM Wiki: this folder has a Wiki/ directory but no llm-wiki.yml — it is not configured. If the user wants to set it up or repair it, that is the \`wiki-setup\` skill (/wiki-setup)."
  fi
  exit 0
fi

# Configured. Surface only what a session genuinely needs up front.
if [ -f "$DIR/wiki-backfill-state.json" ] && grep -q '"status"[[:space:]]*:[[:space:]]*"in_progress"' "$DIR/wiki-backfill-state.json" 2>/dev/null; then
  echo "LLM Wiki: a historical backfill is in progress (see wiki-backfill-state.json). Mention it in one line if relevant; do not derail the user's request."
fi

if ls "$DIR"/**/*conflicted\ copy* "$DIR"/*conflicted\ copy* "$DIR"/**/*.sync-conflict-* 2>/dev/null | head -1 | grep -q .; then
  echo "LLM Wiki: sync conflict copies exist in this folder. Surface them to the user and offer to merge them into the canonical pages. Never delete one. They usually mean more than one machine is running the ingest."
fi

exit 0
