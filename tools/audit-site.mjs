import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ignoredNames = /(?:_template|_old|_incomplete|laplace_formula_example)\.html$/i;
const htmlFiles = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'test_exams') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith('.html') && !ignoredNames.test(entry.name)) htmlFiles.push(full);
  }
}

function exactCaseExists(target) {
  const relative = path.relative(root, target);
  if (relative.startsWith('..')) return false;
  if (!relative) return true;
  let current = root;
  for (const segment of relative.split(path.sep)) {
    const entries = fs.readdirSync(current);
    if (!entries.includes(segment)) return false;
    current = path.join(current, segment);
  }
  return true;
}

walk(root);
const errors = [];
const warnings = [];
let checkedReferences = 0;

for (const file of htmlFiles) {
  const relative = path.relative(root, file).split(path.sep).join('/');
  const html = fs.readFileSync(file, 'utf8');
  const visibleHtml = html.replace(/<!--[\s\S]*?-->/g, '');
  if (!/<meta\s+name=["']viewport["']/i.test(html)) errors.push(`${relative}: viewport meta is missing`);
  if (/\{\{[A-Z0-9_]+\}\}/.test(visibleHtml)) errors.push(`${relative}: unresolved template token`);

  const ids = [...html.matchAll(/\sid=["']([^"']+)["']/gi)].map((match) => match[1]);
  const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index);
  for (const id of new Set(duplicates)) errors.push(`${relative}: duplicate id #${id}`);

  for (const match of html.matchAll(/<(a|link|script|img)\b[^>]*?\s(href|src)=["']([^"']+)["'][^>]*>/gi)) {
    const [tag, element, attribute, rawUrl] = match;
    if (/^(?:https?:|mailto:|tel:|data:|javascript:|#)/i.test(rawUrl)) continue;
    checkedReferences += 1;
    let decoded;
    try { decoded = decodeURIComponent(rawUrl.split(/[?#]/)[0]); }
    catch { errors.push(`${relative}: invalid URL encoding in ${rawUrl}`); continue; }
    if (!decoded) continue;
    const target = decoded.startsWith('/')
      ? path.resolve(root, decoded.slice(1))
      : path.resolve(path.dirname(file), decoded);
    if (!fs.existsSync(target)) errors.push(`${relative}: missing ${attribute} target ${rawUrl}`);
    else if (!exactCaseExists(target)) errors.push(`${relative}: path case mismatch ${rawUrl}`);
    if (element.toLowerCase() === 'a' && /target=["']_blank["']/i.test(tag) && !/rel=["'][^"']*noopener/i.test(tag)) {
      warnings.push(`${relative}: target=_blank should include rel=noopener (${rawUrl})`);
    }
  }

  for (const image of html.matchAll(/<img\b([^>]*)>/gi)) {
    if (!/\salt=["'][^"']*["']/i.test(image[1])) errors.push(`${relative}: image is missing alt attribute`);
  }

  const examMatch = relative.match(/^exams\/(math|fluid|materials|thermo)\/(\d{4})\.html$/);
  if (examMatch) {
    const year = examMatch[2];
    const title = html.match(/<title>([^<]+)<\/title>/i)?.[1] ?? '';
    if (!title.includes(year)) errors.push(`${relative}: title does not contain ${year}`);
  }
}

console.log(`HTML files: ${htmlFiles.length}`);
console.log(`Local references checked: ${checkedReferences}`);
console.log(`Errors: ${errors.length}`);
for (const error of errors) console.log(`ERROR ${error}`);
console.log(`Warnings: ${warnings.length}`);
for (const warning of warnings) console.log(`WARN ${warning}`);

if (errors.length) process.exitCode = 1;
