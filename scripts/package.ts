// Zips each themes/<app>/ into dist/draculinho-<app>.zip for the GitHub release. Run from the repo root after the VSIX build: node scripts/package.ts
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { strToU8, zipSync, type Zippable } from 'fflate';

const { version }: { version: string } = JSON.parse(readFileSync('package.json', 'utf8'));

for (const app of readdirSync('themes', { withFileTypes: true })) {
  if (!app.isDirectory()) continue;
  const dir = join('themes', app.name);
  const files: Zippable = {};
  for (const file of readdirSync(dir, { recursive: true, withFileTypes: true })) {
    if (!file.isFile() || file.name.startsWith('.')) continue;
    const src = join(file.parentPath, file.name);
    files[relative(dir, src).split(sep).join('/')] = readFileSync(src);
  }
  if (app.name === 'chrome') {
    // The Chrome Web Store rejects a version it already has, so this follows the release.
    const manifest = readFileSync(join(dir, 'manifest.json'), 'utf8');
    files['manifest.json'] = strToU8(manifest.replace(/"version": "[^"]*"/, `"version": "${version}"`));
  }
  writeFileSync(join('dist', `draculinho-${app.name}.zip`), zipSync(files));
}
