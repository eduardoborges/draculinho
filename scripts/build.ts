// Renders templates/ into themes/ with the colors in palette.json. Run from the repo root: node scripts/build.ts
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, sep } from 'node:path';

const PALETTE: Record<string, string> = JSON.parse(readFileSync('palette.json', 'utf8'));

const rgb = (h: string) => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));

// Apps that don't take #RRGGBB.
const FORMATS: Record<string, (h: string) => string> = {
  chrome: h => `[${rgb(h).join(', ')}]`,
  'claude-code': h => `rgb(${rgb(h).join(',')})`,
  jetbrains: h => h.slice(1).toLowerCase(),
  xcode: h => rgb(h).map(c => (c / 255).toFixed(6)).join(' '),
};

for (const file of readdirSync('templates', { recursive: true, withFileTypes: true })) {
  if (!file.isFile() || file.name.startsWith('.')) continue;
  const src = join(file.parentPath, file.name);
  const [, app, ...rest] = src.split(sep);
  const fmt = FORMATS[app] ?? String;
  const text = readFileSync(src, 'utf8').replace(/\{\{(\w+)\}\}/g, (_, name: string) => {
    if (!(name in PALETTE)) throw new Error(`${src}: no "${name}" in palette.json`);
    return fmt(PALETTE[name]);
  });
  writeFileSync(join('themes', app, ...rest), text);
}
