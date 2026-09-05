#!/usr/bin/env sh
# Installs Draculinho for the apps you pick.
#   ./install.sh                 interactive menu
#   ./install.sh zed ghostty     install only these
#   ./install.sh all
# Works from a checkout or piped from curl (files come from GitHub main).
set -eu

RAW="https://raw.githubusercontent.com/eduardoborges/draculinho/main/themes"
HERE="$(cd "$(dirname "$0")" 2>/dev/null && pwd || pwd)"
CFG="${XDG_CONFIG_HOME:-$HOME/.config}"
APPS="vscode zed ghostty herdr claude-code"

# theme <app> <file>: prints the local path of a theme file, downloading it when there is no checkout.
theme() {
  if [ -f "$HERE/themes/$1/$2" ]; then
    printf '%s\n' "$HERE/themes/$1/$2"
  else
    tmp="$(mktemp)"
    curl -fsSL "$RAW/$1/$2" -o "$tmp"
    printf '%s\n' "$tmp"
  fi
}

say() { printf '  %s\n' "$*"; }

install_vscode() {
  for bin in code cursor codium; do
    if command -v "$bin" >/dev/null 2>&1; then
      "$bin" --install-extension eduardoborges.draculinho >/dev/null && say "$bin: extension installed"
      found=1
    fi
  done
  [ "${found:-}" ] || say "no code/cursor/codium CLI found. Search for Draculinho in the extension panel."
}

install_zed() {
  mkdir -p "$CFG/zed/themes"
  cp "$(theme zed draculinho.json)" "$CFG/zed/themes/draculinho.json"
  say "copied to $CFG/zed/themes/. Pick it with cmd+k cmd+t or set \"theme\": \"Draculinho\"."
}

install_ghostty() {
  mkdir -p "$CFG/ghostty/themes"
  cp "$(theme ghostty draculinho)" "$CFG/ghostty/themes/draculinho"
  conf="$CFG/ghostty/config"
  touch "$conf"
  if grep -qE '^theme *=' "$conf"; then
    sed -i.bak -E 's/^theme *=.*/theme = draculinho/' "$conf" && rm -f "$conf.bak"
  else
    printf 'theme = draculinho\n' >> "$conf"
  fi
  say "theme = draculinho set in $conf. Reload Ghostty (cmd+shift+, on macOS)."
}

install_herdr() {
  conf="$CFG/herdr/config.toml"
  mkdir -p "$CFG/herdr"
  touch "$conf"
  if grep -q '^\[theme\.custom\]' "$conf"; then
    say "$conf already has [theme.custom]. Merge $RAW/herdr/draculinho.toml by hand."
    return
  fi
  src="$(theme herdr draculinho.toml)"
  if grep -q '^\[theme\]' "$conf"; then
    sed -i.bak -E '/^\[theme\]/,/^\[/ s/^name *=.*/name = "dracula"/' "$conf" && rm -f "$conf.bak"
    { printf '\n'; sed -n '/^\[theme\.custom\]/,$p' "$src"; } >> "$conf"
  else
    { printf '\n'; grep -v '^#' "$src"; } >> "$conf"
  fi
  say "[theme.custom] added to $conf on top of dracula."
  if command -v herdr >/dev/null 2>&1; then
    herdr config check >/dev/null 2>&1 || say "warning: herdr config check failed, review $conf"
    herdr server reload-config >/dev/null 2>&1 && say "herdr reloaded" || say "start herdr to see it"
  fi
}

install_claude_code() {
  dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  mkdir -p "$dir/themes"
  cp "$(theme claude-code draculinho.json)" "$dir/themes/draculinho.json"
  settings="$dir/settings.json"
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$settings" <<'PY'
import json, sys, os
p = sys.argv[1]
d = json.load(open(p)) if os.path.exists(p) else {}
d["theme"] = "custom:draculinho"
json.dump(d, open(p, "w"), indent=2); open(p, "a").write("\n")
PY
    say "theme set to custom:draculinho in $settings. Takes effect on the next session."
  else
    say "copied to $dir/themes/. Pick Draculinho with /theme."
  fi
}

pick() {
  i=1
  for a in $APPS; do printf '  %d) %s\n' "$i" "$a"; i=$((i + 1)); done
  printf '  a) all\n\nInstall which? (numbers separated by spaces) '
  read -r answer </dev/tty
  case "$answer" in
    a|all|"") printf '%s\n' "$APPS" ;;
    *) for n in $answer; do
         i=1
         for a in $APPS; do [ "$i" = "$n" ] && printf '%s ' "$a"; i=$((i + 1)); done
       done; printf '\n' ;;
  esac
}

if [ "$#" -eq 0 ]; then
  printf 'Draculinho installer\n\n'
  chosen="$(pick)"
elif [ "$1" = "all" ]; then
  chosen="$APPS"
else
  chosen="$*"
fi

for app in $chosen; do
  case " $APPS " in
    *" $app "*) printf '\n%s\n' "$app"; "install_$(printf '%s' "$app" | tr - _)" ;;
    *) printf '\nunknown app: %s (options: %s)\n' "$app" "$APPS" >&2; exit 1 ;;
  esac
done
printf '\n'
