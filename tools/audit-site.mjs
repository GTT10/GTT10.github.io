import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
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
  for (const phrase of ['HTML解説', 'ブラウザで解説', '非公式', 'accuracy-notice']) {
    if (visibleHtml.includes(phrase)) errors.push(`${relative}: removed interface wording remains (${phrase})`);
  }

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

  let inlineScriptIndex = 0;
  for (const script of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attributes = script[1];
    const source = script[2].trim();
    if (!source || /\ssrc=["']/i.test(attributes) || /\stype=["'](?:application\/ld\+json|application\/json)["']/i.test(attributes)) continue;
    try {
      new vm.Script(source, { filename: `${relative}:inline-${inlineScriptIndex}` });
    } catch (error) {
      errors.push(`${relative}: inline JavaScript syntax error (${error.message})`);
    }
    inlineScriptIndex += 1;
  }

  const examMatch = relative.match(/^exams\/(math|fluid|materials|thermo)\/(\d{4})\.html$/);
  if (examMatch) {
    const year = examMatch[2];
    const title = html.match(/<title>([^<]+)<\/title>/i)?.[1] ?? '';
    if (!title.includes(year)) errors.push(`${relative}: title does not contain ${year}`);
  }
}

const examFiles = htmlFiles.filter((file) => /^exams\/(?:math|fluid|materials|thermo)\/\d{4}\.html$/.test(
  path.relative(root, file).split(path.sep).join('/'),
));
const archiveExamFiles = examFiles.filter((file) => fs.readFileSync(file, 'utf8').includes('data-page-status="archive"'));
const detailedExamFiles = examFiles.filter((file) => !archiveExamFiles.includes(file));
if (examFiles.length !== 88) errors.push(`exam inventory: expected 88 pages, found ${examFiles.length}`);

const indexHtml = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const aboutHtml = fs.readFileSync(path.join(root, 'about.html'), 'utf8');
if (!indexHtml.includes(`<dt>解説</dt><dd>${detailedExamFiles.length}</dd>`)) {
  errors.push(`index.html: explanation count is not ${detailedExamFiles.length}`);
}
if (!aboutHtml.includes(`${detailedExamFiles.length}年度分は解説付き`) || !aboutHtml.includes(`${archiveExamFiles.length}年度分はPDF資料のみ`)) {
  errors.push(`about.html: coverage counts do not match ${detailedExamFiles.length} detailed / ${archiveExamFiles.length} archive pages`);
}

const migratedDetailedPages = [
  ['exams/math/2003.html', 'math.css'],
  ...Array.from({ length: 6 }, (_, index) => [`exams/fluid/${2003 + index}.html`, 'fluid.css']),
  ...Array.from({ length: 6 }, (_, index) => [`exams/materials/${2003 + index}.html`, 'materials.css']),
];
for (const [relative, stylesheet] of migratedDetailedPages) {
  const html = fs.readFileSync(path.join(root, relative), 'utf8');
  if (!html.includes(`../../css/${stylesheet}`)) errors.push(`${relative}: subject stylesheet ${stylesheet} is missing`);
  if (html.includes('../../css/archive.css')) errors.push(`${relative}: legacy archive stylesheet remains`);
  if (!html.includes('id="MathJax-script"')) errors.push(`${relative}: MathJax renderer is missing`);
  if (!html.includes('class="exam-grid')) errors.push(`${relative}: subject exam layout is missing`);
  if (html.indexOf('window.MathJax') > html.indexOf('id="MathJax-script"')) errors.push(`${relative}: MathJax configuration loads too late`);
  if (html.includes('class="formula"')) errors.push(`${relative}: legacy formula markup remains`);
  const body = html.split('<body>', 2)[1] ?? '';
  const asciiDelimiters = (body.match(/`/g) ?? []).length;
  if (asciiDelimiters % 2 !== 0) errors.push(`${relative}: unmatched AsciiMath delimiter`);
}

const contentRequirements = {
  'exams/math/2003.html': ['100万倍', '0.69', '\\nabla^2\\mathbf A', '\\tanh(as/2)'],
  'exams/fluid/2003.html': ['糸端は空間に固定', 'B=1 gf', 'v=0.5 cm/s', '二次元微小検査領域', 'Strouhal数', 'Euler数'],
  'exams/thermo/2003.html': ['散逸機構', '曲線を描く答えは一意ではありません'],
  'exams/thermo/2007.html': ['排気温度 \\(T_2\\) は一意に定まりません', '\\kappa(T)=1+R/(\\alpha T)', '分子量', '\\Delta S_{\\mathrm{sensible}}'],
};
for (const [relative, phrases] of Object.entries(contentRequirements)) {
  const html = fs.readFileSync(path.join(root, relative), 'utf8');
  for (const phrase of phrases) {
    if (!html.includes(phrase)) errors.push(`${relative}: required audited content is missing (${phrase})`);
  }
}

const forbiddenContent = {
  'exams/fluid/2003.html': ['流線に沿う微小流管', 'A(s,t)'],
  'about.html': ['別担当による再検算', '全88年度分の全大問・全小問を問題PDFの条件から独立に再計算'],
  'statistics.html': ['event.target.closest', '空ファイル（内容不明）', '省略版', 'Chart.js'],
};
for (const [relative, phrases] of Object.entries(forbiddenContent)) {
  const html = fs.readFileSync(path.join(root, relative), 'utf8');
  for (const phrase of phrases) {
    if (html.includes(phrase)) errors.push(`${relative}: stale or misleading content remains (${phrase})`);
  }
}

const statisticsHtml = fs.readFileSync(path.join(root, 'statistics.html'), 'utf8');
for (const phrase of ['20/22', '21/22', '大問 1.80', '大問 2.00', '小問 11.20', '勉強する順番']) {
  if (!statisticsHtml.includes(phrase)) errors.push(`statistics.html: decisive trend evidence is missing (${phrase})`);
}

console.log(`HTML files: ${htmlFiles.length}`);
console.log(`Exam pages: ${examFiles.length} (${detailedExamFiles.length} detailed, ${archiveExamFiles.length} archive)`);
console.log(`Local references checked: ${checkedReferences}`);
console.log(`Errors: ${errors.length}`);
for (const error of errors) console.log(`ERROR ${error}`);
console.log(`Warnings: ${warnings.length}`);
for (const warning of warnings) console.log(`WARN ${warning}`);

if (errors.length) process.exitCode = 1;
