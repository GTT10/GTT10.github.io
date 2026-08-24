import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const examRoot = path.join(root, 'exams');
const subjects = ['math', 'fluid', 'materials', 'thermo'];
const marker = 'class="accuracy-notice"';
let updated = 0;

for (const subject of subjects) {
  const directory = path.join(examRoot, subject);

  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (!entry.isFile() || !/^\d{4}\.html$/.test(entry.name)) continue;

    const file = path.join(directory, entry.name);
    const html = fs.readFileSync(file, 'utf8');
    if (!html.includes('class="problem-overview-section"') || html.includes(marker)) continue;

    const newline = html.includes('\r\n') ? '\r\n' : '\n';
    const notice = [
      '                <aside class="accuracy-notice" role="note">',
      '                    <strong>非公式の解説です。</strong>',
      '                    数式・数値・図表は、問題原本と信頼できる資料で必ず確認してください。',
      '                </aside>',
    ].join(newline);
    const next = html.replace(
      /(<div class="problem-overview-section">)/,
      `$1${newline}${notice}`,
    );

    fs.writeFileSync(file, next, 'utf8');
    updated += 1;
  }
}

console.log(`Added accuracy notices to ${updated} detailed exam pages.`);
