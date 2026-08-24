import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const status = execFileSync('git', ['status', '--porcelain', '-z'], {
  cwd: root,
  encoding: 'utf8',
});
const textExtensions = new Set(['.css', '.html', '.js', '.mjs', '.txt', '.xml']);
const files = status
  .split('\0')
  .filter(Boolean)
  .map((record) => record.slice(3))
  .filter((relative) => textExtensions.has(path.extname(relative).toLowerCase()));

for (const relative of files) {
  const file = path.join(root, relative);
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) continue;

  const source = fs.readFileSync(file, 'utf8');
  const normalized = source
    .replace(/\r\n?/g, '\n')
    .split('\n')
    .map((line) => line.replace(/[\t ]+$/g, ''))
    .join('\n')
    .replace(/\n*$/, '\n');
  fs.writeFileSync(file, normalized, 'utf8');
}

console.log(`Normalized ${files.length} modified text files.`);
