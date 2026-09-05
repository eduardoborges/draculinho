#!/usr/bin/env python3
"""Renders the README previews with headless Chrome. Run from the repo root: python3 scripts/previews.py"""
import html, os, re, subprocess

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = "assets"
BG, FG, MUTED, SEL, SURF = "#0E131B", "#CDD0DD", "#465276", "#44475A", "#21222C"
CYAN, GREEN, ORANGE, PINK, PURPLE, RED, YELLOW = "#00B5DC", "#3dcf62", "#FFB86C", "#FF79C6", "#BD93F9", "#FF5555", "#E2DD61"
QUOTE, TAGP = "#E9F284", "#b65f8f"

# Token classes follow the VS Code theme: [[k:const]] -> keyword, pink italic.
TOKENS = {
    "k": f"color:{PINK};font-style:italic",       # keyword, storage
    "o": f"color:{PINK}",                          # =, =>, ===
    "f": f"color:{GREEN}",                         # function
    "a": f"color:{GREEN};font-style:italic",       # attribute, decorator, css class
    "p": f"color:{ORANGE};font-style:italic",      # parameter
    "t": f"color:{CYAN};font-style:italic",        # type, built-in
    "c": f"color:{CYAN}",                          # class name, property-name (css/json key)
    "s": f"color:{YELLOW}",                        # string
    "q": f"color:{QUOTE}",                         # string quotes
    "n": f"color:{PURPLE}",                        # constant, number, boolean
    "th": f"color:{PURPLE};font-style:italic",     # this, self
    "m": f"color:{MUTED}",                         # comment
    "g": f"color:{PINK}",                          # tag
    "gp": f"color:{TAGP}",                         # tag punctuation
    "x": f"color:{FG}",
    "r": f"color:{RED}", "y": f"color:{YELLOW}", "pu": f"color:{PURPLE}", "cy": f"color:{CYAN}", "gr": f"color:{GREEN}", "or": f"color:{ORANGE}",
    "b": "font-weight:700",
}

def span(kind, text):
    if kind == "s" and text[:1] in "'\"`" and text[-1:] == text[:1]:
        q = f'<span style="{TOKENS["q"]}">{text[0]}</span>'
        return f'{q}<span style="{TOKENS["s"]}">{text[1:-1]}</span>{q}'
    return f'<span style="{TOKENS[kind]}">{text}</span>'

def mark(src):
    return re.sub(r"\[\[(\w+):(.*?)\]\]", lambda m: span(m.group(1), m.group(2)), html.escape(src), flags=re.S)

TSX = """[[k:import]] { [[t:useState]] } [[k:from]] [[s:'react']];
[[k:import]] [[k:type]] { [[t:Theme]] } [[k:from]] [[s:'./theme']];

[[m:// Toggles between the dark and light palettes.]]
[[k:export]] [[k:const]] [[f:ThemeSwitch]] [[o:=]] ({ [[p:initial]], [[p:onChange]] }: [[t:Props]]) [[o:=>]] {
  [[k:const]] [theme, setTheme] [[o:=]] [[t:useState]]<[[t:Theme]]>(initial);
  [[k:const]] isDark [[o:=]] theme.mode [[o:===]] [[s:'dark']];

  [[k:const]] [[f:toggle]] [[o:=]] () [[o:=>]] {
    [[k:const]] next [[o:=]] { ...theme, mode: isDark [[k:?]] [[s:'light']] [[k::]] [[s:'dark']] };
    [[f:setTheme]](next);
    onChange?.(next);
  };

  [[k:return]] (
    [[gp:<]][[g:button]] [[a:className]][[o:=]][[s:"switch"]] [[a:onClick]][[o:=]]{toggle} [[a:aria-pressed]][[o:=]]{isDark}[[gp:>]]
      {isDark [[k:?]] [[s:'🌙']] [[k::]] [[s:'☀️']]} {theme.name}
    [[gp:</]][[g:button]][[gp:>]]
  );
};

[[k:export]] [[k:default]] [[k:class]] [[c:Palette]] {
  [[k:static]] [[k:readonly]] [[n:BACKGROUND]] [[o:=]] [[s:'#0E131B']];

  [[k:constructor]]([[k:private]] [[p:colors]]: [[t:Map]]<[[t:string]], [[t:string]]>) {}

  [[f:get]]([[p:name]]: [[t:string]]): [[t:string]] {
    [[k:return]] [[th:this]].colors.get(name) [[k:??]] [[c:Palette]].[[n:BACKGROUND]];
  }
}"""

CSS = """[[m:/* Dracula, a few shades darker */]]
[[k::root]] {
  [[c:--bg]]: [[n:#0E131B]];
  [[c:--fg]]: [[n:#CDD0DD]];
  [[c:--accent]]: [[n:#BD93F9]];
}

[[g:body]] {
  [[c:background]]: [[f:var]]([[c:--bg]]);
  [[c:color]]: [[f:var]]([[c:--fg]]);
  [[c:font-family]]: [[s:"Dank Mono"]], [[n:monospace]];
  [[c:line-height]]: [[n:1.6]];
}

[[a:.switch]][[k::hover]] {
  [[c:color]]: [[f:var]]([[c:--accent]]);
  [[c:transform]]: [[f:translateY]]([[n:-1px]]);
  [[c:transition]]: [[n:all]] [[n:150ms]] [[n:ease-out]];
}

[[k:@media]] ([[c:prefers-color-scheme]]: [[n:light]]) {
  [[g:body]] { [[c:filter]]: [[f:invert]]([[n:1]]) [[k:!important]]; }
}"""

TERMINAL = """[[cy:~/Projects/draculinho]] [[pu: main]] [[m:v1.3.0]]
[[gr:❯]] git log --oneline -4
[[y:328531a]] [[b:fix(claude-code):]] orange spinner while working
[[y:a49608f]] [[b:ci:]] publish the Chrome theme to the Web Store
[[y:f263a4e]] [[b:feat:]] add Chrome theme
[[y:3790b67]] [[b:feat:]] add install script with app selection

[[gr:❯]] git status --short
[[gr: M]] README.md
[[gr:A ]] assets/preview-terminal.png
[[r:??]] scripts/previews.py

[[gr:❯]] sh install.sh zed ghostty herdr claude-code
[[or:✻]] [[or:Installing…]]"""

ANSI = [("#21222C", "black"), (RED, "red"), (GREEN, "green"), (YELLOW, "yellow"), (PURPLE, "blue"), (PINK, "magenta"), (CYAN, "cyan"), (FG, "white"),
        (MUTED, ""), ("#FF6E6E", ""), ("#69FF94", ""), ("#FFFFA5", ""), ("#D6ACFF", ""), ("#FF92DF", ""), ("#A4FFFF", ""), ("#FFFFFF", "")]

PALETTE = [(BG, "Background"), (FG, "Foreground"), (PURPLE, "Purple"), (PINK, "Pink"), (CYAN, "Cyan"), (GREEN, "Green"), (ORANGE, "Orange"), (RED, "Red"), (YELLOW, "Yellow"), (MUTED, "Comment")]

STYLE = f"""
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: transparent; }}
body {{ padding: 28px; display: inline-block; }}
.win {{ background: {BG}; border-radius: 14px; box-shadow: 0 24px 60px rgba(0,0,0,.45), 0 0 0 1px rgba(255,255,255,.06); overflow: hidden; }}
.bar {{ height: 44px; display: flex; align-items: center; gap: 8px; padding: 0 18px; background: {SURF}; }}
.dot {{ width: 12px; height: 12px; border-radius: 50%; }}
.title {{ margin-left: auto; margin-right: auto; color: {MUTED}; font: 13px -apple-system, "SF Pro Text", sans-serif; }}
pre {{ margin: 0; padding: 26px 30px 30px; font: 15px/1.7 "Dank Mono", "DankMono Nerd Font", monospace; color: {FG}; tab-size: 2; }}
.ln {{ display: inline-block; width: 2.2em; color: {MUTED}; text-align: right; margin-right: 1.6em; user-select: none; }}
"""

def window(title, body, width):
    return f"""<meta charset="utf-8"><style>{STYLE}</style>
<div class="win" style="width:{width}px">
  <div class="bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span><span class="title">{title}</span></div>
  {body}
</div>"""

def code(src, numbered=True):
    lines = mark(src).split("\n")
    if numbered:
        lines = [f'<span class="ln">{i}</span>{l}' for i, l in enumerate(lines, 1)]
    return "<pre>" + "\n".join(lines) + "</pre>"

def ansi_grid():
    cells = "".join(f'<div style="background:{c};height:26px;border-radius:5px"></div>' for c, _ in ANSI)
    return f'<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:8px;padding:0 30px 30px">{cells}</div>'

def palette():
    sw = "".join(
        f'<div style="flex:1"><div style="background:{c};height:72px;border-radius:12px;box-shadow:0 0 0 1px rgba(255,255,255,.08) inset"></div>'
        f'<div style="margin-top:10px;color:{FG};font:600 13px -apple-system,sans-serif">{n}</div>'
        f'<div style="color:{MUTED};font:12px \'Dank Mono\',monospace">{c.upper()}</div></div>'
        for c, n in PALETTE)
    return f'<meta charset="utf-8"><style>{STYLE}</style><div class="win" style="width:1080px;padding:30px;display:flex;gap:14px">{sw}</div>'

def shoot(name, markup, width, height):
    path = f"{OUT}/{name}.html"
    open(path, "w").write(markup)
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=2", "--default-background-color=00000000",
                    f"--window-size={width + 56},{height + 56}", f"--screenshot={OUT}/{name}.png", os.path.abspath(path)],
                   check=True, capture_output=True)
    os.remove(path)
    print("wrote", f"{OUT}/{name}.png")

def h(lines, extra=0):  # window height from line count
    return 44 + 56 + round(lines * 15 * 1.7) + extra

os.makedirs(OUT, exist_ok=True)
shoot("preview-tsx", window("ThemeSwitch.tsx", code(TSX), 900), 900, h(TSX.count("\n") + 1))
shoot("preview-css", window("theme.css", code(CSS), 760), 760, h(CSS.count("\n") + 1))
shoot("preview-terminal", window("ghostty", code(TERMINAL, numbered=False) + ansi_grid(), 760), 760, h(TERMINAL.count("\n") + 1, 60))
shoot("palette", palette(), 1080, 190)
