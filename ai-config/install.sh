#!/usr/bin/env bash
set -euo pipefail

claude_dir="${CLAUDE_DIR:-$HOME/.claude}"
force=""
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(dirname "$here")"

case "${1:-}" in
  "") ;;
  --force) force="--force" ;;
  *) echo "usage: install.sh [--force]" >&2; exit 1 ;;
esac

install_file() {
  local source="$1" target="$2"
  if [[ ! -e "$target" ]]; then
    mkdir -p "$(dirname "$target")"
    cp "$source" "$target"
    echo "installed"
  elif cmp -s "$source" "$target"; then
    echo "unchanged"
  elif [[ -z "$force" ]]; then
    echo "skipped (differs, use --force)"
  else
    cp "$target" "$target.bak-$(date +%Y%m%d%H%M%S)"
    cp "$source" "$target"
    echo "replaced (backup kept)"
  fi
}

report() {
  local name="$1" source="$2" target="$3" status
  status="$(install_file "$source" "$target")"
  printf '%-28s %s\n' "$name" "$status"
}

report "CLAUDE.md" "$here/CLAUDE.md" "$claude_dir/CLAUDE.md"
for agent in "$repo_root"/.claude/agents/*.md; do
  name="$(basename "$agent")"
  report "$name" "$agent" "$claude_dir/agents/$name"
done
echo "Merge ai-config/settings.snippet.json into $claude_dir/settings.json by hand."
