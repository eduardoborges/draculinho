<div align="center">

<img src="./assets/logo.png" width="100" />

# Draculinho

A darker, moodier take on the classic [Dracula](https://draculatheme.com) theme. Crafted for ligature fonts and italic lovers.

[![Version](https://img.shields.io/visual-studio-marketplace/v/eduardoborges.draculinho?style=flat-square&label=VS%20Code&colorA=0E131B&colorB=BD93F9)](https://marketplace.visualstudio.com/items?itemName=eduardoborges.draculinho)
[![Open VSX](https://img.shields.io/open-vsx/v/eduardoborges/draculinho?style=flat-square&label=Open%20VSX&colorA=0E131B&colorB=FF79C6)](https://open-vsx.org/extension/eduardoborges/draculinho)
[![License](https://img.shields.io/github/license/eduardoborges/draculinho?style=flat-square&colorA=0E131B&colorB=3dcf62)](./LICENSE.md)

</div>

---

## Preview

**JavaScript**

![JavaScript example](./assets/js-example.png)

**React / TSX**

![TSX example](./assets/tsx-example.png)

**CSS**

![CSS example](./assets/css-example.png)

## Color Palette

| Color          | Hex       | Preview |
|----------------|-----------|---------|
| Background     | `#0E131B` | ![#0E131B](https://img.shields.io/badge/%20%20-0E131B?style=flat-square&color=0E131B) |
| Foreground     | `#CDD0DD` | ![#CDD0DD](https://img.shields.io/badge/%20%20-CDD0DD?style=flat-square&color=CDD0DD) |
| Purple         | `#BD93F9` | ![#BD93F9](https://img.shields.io/badge/%20%20-BD93F9?style=flat-square&color=BD93F9) |
| Pink           | `#FF79C6` | ![#FF79C6](https://img.shields.io/badge/%20%20-FF79C6?style=flat-square&color=FF79C6) |
| Cyan           | `#00B5DC` | ![#00B5DC](https://img.shields.io/badge/%20%20-00B5DC?style=flat-square&color=00B5DC) |
| Green          | `#3dcf62` | ![#3dcf62](https://img.shields.io/badge/%20%20-3dcf62?style=flat-square&color=3dcf62) |
| Orange         | `#FFB86C` | ![#FFB86C](https://img.shields.io/badge/%20%20-FFB86C?style=flat-square&color=FFB86C) |
| Red            | `#FF5555` | ![#FF5555](https://img.shields.io/badge/%20%20-FF5555?style=flat-square&color=FF5555) |
| Yellow         | `#E2DD61` | ![#E2DD61](https://img.shields.io/badge/%20%20-E2DD61?style=flat-square&color=E2DD61) |
| Comment        | `#465276` | ![#465276](https://img.shields.io/badge/%20%20-465276?style=flat-square&color=465276) |

## Install

### VS Code, Cursor and VSCodium

| Editor   | Link |
|----------|------|
| VS Code  | [`ext install eduardoborges.draculinho`](https://marketplace.visualstudio.com/items?itemName=eduardoborges.draculinho) |
| Cursor   | [`ext install eduardoborges.draculinho`](https://open-vsx.org/extension/eduardoborges/draculinho) |
| VSCodium | [`ext install eduardoborges.draculinho`](https://open-vsx.org/extension/eduardoborges/draculinho) |

Or search for **Draculinho** in your editor's extension panel.

### Zed

Copy [`themes/zed/draculinho.json`](./themes/zed/draculinho.json) to `~/.config/zed/themes/` and set the theme in your settings:

```json
{ "theme": { "mode": "dark", "dark": "Draculinho" } }
```

### Ghostty

Copy [`themes/ghostty/draculinho`](./themes/ghostty/draculinho) to `~/.config/ghostty/themes/` and add this line to your config:

```
theme = draculinho
```

Reload the config afterwards (cmd+shift+, on macOS).

### Herdr

Herdr has no theme files. Draculinho is a set of `[theme.custom]` overrides on top of the built-in `dracula` theme. Copy the contents of [`themes/herdr/draculinho.toml`](./themes/herdr/draculinho.toml) into `~/.config/herdr/config.toml`, then run:

```sh
herdr server reload-config
```

### Claude Code

Copy [`themes/claude-code/draculinho.json`](./themes/claude-code/draculinho.json) to `~/.claude/themes/` and pick Draculinho in `/theme`. You can also set it directly in `~/.claude/settings.json`:

```json
{ "theme": "custom:draculinho" }
```

## Recommended Setup

This theme was designed with ligature and italic fonts in mind. For the best experience, try one of these fonts:

- [Dank Mono](https://philpl.gumroad.com/l/dank-mono) — ligatures and beautiful italics, made for code
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- [Fira Code](https://github.com/tonsky/FiraCode)
- [Cascadia Code](https://github.com/microsoft/cascadia-code)

Then enable ligatures and italic rendering in your `settings.json`:

```json
{
  "editor.fontLigatures": true,
  "editor.tokenColorCustomizations": {
    "[Draculinho]": {
      "textMateRules": [
        {
          "scope": "comment",
          "settings": { "fontStyle": "italic" }
        }
      ]
    }
  }
}
```

## What Makes It Different

Draculinho keeps the Dracula DNA but pushes the background **much darker** (`#0E131B` vs the original `#282A36`), giving a deeper, more focused feel — especially on OLED displays. Keywords, storage types, and special variables render in *italic*, making the code structure stand out at a glance.

## License

[MIT](./LICENSE.md) — based on the original [Dracula Theme](https://github.com/dracula/dracula-theme) by Zeno Rocha.
