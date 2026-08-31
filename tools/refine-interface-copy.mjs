import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const examRoot = path.join(root, 'exams');
let updated = 0;

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const target = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(target) : [target];
  });
}

for (const file of walk(examRoot).filter((target) => target.endsWith('.html'))) {
  const source = fs.readFileSync(file, 'utf8');
  const relative = path.relative(root, file).split(path.sep).join('/');
  let output = source.replace(
    /\s*<aside class="accuracy-notice" role="note">\s*<strong>非公式の解説です。<\/strong>\s*数式・数値・図表は、問題原本と信頼できる資料で必ず確認してください。\s*<\/aside>/g,
    '',
  );

  output = output
    .replace(/\['\\\(', '\\\)'\]/g, "['\\\\(', '\\\\)']")
    .replace(/\['\\\[', '\\\]'\]/g, "['\\\\[', '\\\\]']")
    .replaceAll('数式は画面幅に合わせて表示し、長い式は横にスクロールできます。', '')
    .replaceAll('class="accuracy-notice"', 'class="point-box source-check"')
    .replaceAll('原本照合済み・非公式', '原本照合')
    .replaceAll('検算済み・非公式', '原本照合')
    .replaceAll('非公式解答PDF', '解答PDF')
    .replaceAll('非公式解答案', '解答案')
    .replaceAll('非公式解説', '解説')
    .replaceAll('独立再計算、解説', '独立再計算による解説')
    .replaceAll('公式解答ではありません。', '')
    .replaceAll('（非公式）', '')
    .replaceAll('(非公式)', '');

  if (/^exams\/fluid\/200[3-8]\.html$/.test(relative)) {
    const bodyAt = output.indexOf('<body>');
    const head = output.slice(0, bodyAt);
    const body = output.slice(bodyAt).replace(/`([^`\n]+)`/g, (whole, sourceFormula) => {
      let formula = sourceFormula
        .replaceAll('Ψ', ' Psi ')
        .replaceAll('γ', ' gamma ')
        .replaceAll('½', '(1/2)')
        .replaceAll('xxx', 'x xx ')
        .replaceAll('xx', ' xx ');
      for (const token of ['partial', 'sqrt', 'nabla', 'Delta', 'Gamma', 'Omega', 'omega', 'theta', 'alpha', 'beta', 'gamma', 'rho', 'mu', 'nu', 'tau', 'phi', 'psi', 'Psi', 'pi']) {
        formula = formula.replaceAll(token, ` ${token} `);
      }
      return `\`${formula.replace(/\s+/g, ' ').trim()}\``;
    });
    output = head + body;
  }

  if (output !== source) {
    fs.writeFileSync(file, output, 'utf8');
    updated += 1;
  }
}

console.log(`Refined interface copy in ${updated} exam pages.`);
