import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const years = Array.from({ length: 22 }, (_, index) => 2024 - index);
const subjects = {
  math: {
    name: '数学',
    page: 'math.html',
    icon: 'math_icon.png',
    css: 'math.css',
    description: '微分積分、線形代数、微分方程式、ベクトル解析などを年度別に確認できます。',
  },
  fluid: {
    name: '流体力学',
    page: 'fluid_mechanics.html',
    icon: 'fluid_mechanics_icon.png',
    css: 'fluid.css',
    description: '静水力学、ベルヌーイの定理、粘性流れ、運動量保存などを年度別に確認できます。',
  },
  materials: {
    name: '材料力学',
    page: 'material_mechanics.html',
    icon: 'material_mechanics_icon.png',
    css: 'materials.css',
    description: '応力とひずみ、はりの曲げ、ねじり、座屈などを年度別に確認できます。',
  },
  thermo: {
    name: '熱力学',
    page: 'thermodynamics.html',
    icon: 'thermodynamics_icon.png',
    css: 'thermo.css',
    description: '熱力学の法則、状態変化、各種サイクル、伝熱などを年度別に確認できます。',
  },
};

const toWebPath = (value) => value.split(path.sep).join('/');

function findPdf(kind, subject, year) {
  const base = path.join(root, 'pdfs', kind);
  if (!fs.existsSync(base)) return null;
  for (const dirent of fs.readdirSync(base, { withFileTypes: true })) {
    if (!dirent.isDirectory() || !dirent.name.startsWith(String(year))) continue;
    const folder = path.join(base, dirent.name);
    const candidates = fs.readdirSync(folder).filter((name) => {
      const lower = name.toLowerCase();
      const subjectMatch = subject === 'math'
        ? lower.includes('math')
        : lower.includes(subject);
      return lower.endsWith('.pdf') && subjectMatch && lower.includes(String(year));
    });
    if (candidates.length) {
      return toWebPath(path.relative(root, path.join(folder, candidates[0])));
    }
  }
  return null;
}

function eraLabel(questionPath, year) {
  const folder = questionPath?.split('/').at(-2) ?? '';
  const parts = folder.split('_');
  const era = parts.filter((part) => /^[HR]\d+$/.test(part)).join('・');
  return era ? `${year}年度（${era}）` : `${year}年度`;
}

function archivePage(subject, year, questionPath, answerPath) {
  const config = subjects[subject];
  const label = eraLabel(questionPath, year);
  const previous = year > 2003 ? year - 1 : null;
  const next = year < 2024 ? year + 1 : null;
  const answerBlock = answerPath
    ? `<a class="resource-card resource-card--answer" href="../../${answerPath}" target="_blank" rel="noopener">
          <span class="resource-kicker">非公式解答案</span>
          <strong>解答PDFを開く</strong>
          <span>内容をうのみにせず、式と単位を確認しながら利用してください。</span>
        </a>`
    : `<div class="resource-card resource-card--unavailable" aria-label="解答・解説は未収録です">
          <span class="resource-kicker">未収録</span>
          <strong>解答・解説は準備中です</strong>
          <span>現時点では原本問題PDFのみ閲覧できます。</span>
        </div>`;

  return `<!DOCTYPE html>
<html lang="ja" data-page-status="archive">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="岡山大学大学院入試 ${config.name} ${year}年度の過去問資料ページ。問題PDF${answerPath ? 'と非公式解答案' : ''}を収録しています。">
  <title>${config.name} ${year}年度 過去問・資料 - 岡山大学大学院入試アーカイブ</title>
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="../../css/archive.css">
</head>
<body>
  <header class="header header--static">
    <div class="container header-content">
      <a class="logo logo-link" href="../../index.html">岡山大学大学院入試アーカイブ</a>
      <nav class="nav" aria-label="主要ナビゲーション">
        <ul class="nav-list">
          <li><a href="../../index.html" class="nav-link">ホーム</a></li>
          <li><a href="../../pages/${config.page}" class="nav-link">${config.name}一覧</a></li>
          <li><a href="../../about.html" class="nav-link">サイトについて</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <nav class="breadcrumb breadcrumb--static" aria-label="パンくずリスト">
      <div class="container"><a href="../../index.html">ホーム</a><span aria-hidden="true">/</span><a href="../../pages/${config.page}">${config.name}</a><span aria-hidden="true">/</span><span>${year}年度</span></div>
    </nav>

    <section class="archive-hero">
      <div class="container archive-hero__inner">
        <p class="eyebrow">${label}・過去問資料</p>
        <h1>${config.name} ${year}年度</h1>
        <p>${config.description}</p>
        <div class="status-line"><span class="status-badge ${answerPath ? 'status-badge--available' : 'status-badge--limited'}">${answerPath ? '問題・非公式解答案あり' : '問題PDFのみ'}</span><span>原本を優先してご確認ください</span></div>
      </div>
    </section>

    <section class="archive-content">
      <div class="container archive-layout">
        <div>
          <h2>収録資料</h2>
          <div class="resource-grid">
            <a class="resource-card resource-card--question" href="../../${questionPath}" target="_blank" rel="noopener">
              <span class="resource-kicker">原本</span>
              <strong>問題PDFを開く</strong>
              <span>別タブで表示します。印刷や保存はPDF画面から行えます。</span>
            </a>
            ${answerBlock}
          </div>

          <section class="study-guide" aria-labelledby="study-guide-title">
            <h2 id="study-guide-title">この年度に取り組むときの確認手順</h2>
            <ol>
              <li>問題PDFを開き、試験時間を決めて最初に自力で解く。</li>
              <li>記号、仮定、単位、符号規約を答案の冒頭で明確にする。</li>
              <li>${answerPath ? '非公式解答案と照合し、途中式や別解も自分で検算する。' : '教科書や講義資料を使って解法を検算し、自分用の解説をまとめる。'}</li>
            </ol>
          </section>
        </div>

        <aside class="archive-note">
          <h2>利用上の注意</h2>
          <p>このサイトは非公式の学習用アーカイブです。大学公式の掲載物ではありません。</p>
          <p>${answerPath ? '解答案は未検証の箇所を含む可能性があります。数式、数値、図表は原本と照合してください。' : 'この年度の解答・解説は未収録です。内容を推測して掲載していません。'}</p>
          <a href="../../about.html">詳しい利用案内を見る</a>
        </aside>
      </div>
    </section>

    <nav class="year-pagination container" aria-label="年度間ナビゲーション">
      ${previous ? `<a href="${previous}.html">← ${previous}年度</a>` : '<span></span>'}
      <a href="../../pages/${config.page}">年度一覧</a>
      ${next ? `<a href="${next}.html">${next}年度 →</a>` : '<span></span>'}
    </nav>
  </main>

  <footer class="footer">
    <div class="container">
      <p class="footer-text">非公式・学習目的の岡山大学大学院入試アーカイブ</p>
      <p class="footer-subtext">問題・解答案の正確性は必ず原本および信頼できる資料で確認してください。</p>
    </div>
  </footer>
</body>
</html>
`;
}

function subjectPage(subject) {
  const config = subjects[subject];
  const cards = years.map((year) => {
    const examPath = path.join(root, 'exams', subject, `${year}.html`);
    const content = fs.readFileSync(examPath, 'utf8');
    const archive = content.includes('data-page-status="archive"');
    const questionPath = findPdf('question', subject, year);
    const answerPath = findPdf('answer', subject, year);
    const status = archive
      ? (answerPath ? '問題・解答案' : '問題のみ')
      : 'HTML解説あり';
    const statusClass = archive
      ? (answerPath ? 'year-status--answer' : 'year-status--question')
      : 'year-status--html';
    return `
      <article class="year-card">
        <div class="year-card__heading">
          <h2 class="year-title">${year}年度</h2>
          <span class="year-status ${statusClass}">${status}</span>
        </div>
        <div class="exam-links">
          <a href="../exams/${subject}/${year}.html" class="exam-link problem">${archive ? '年度資料を見る' : 'HTML解説を見る'}</a>
          <a href="../${questionPath}" class="exam-link solution" target="_blank" rel="noopener">問題PDF</a>
        </div>
      </article>`;
  }).join('');

  return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="岡山大学大学院入試 ${config.name}の2003年度から2024年度までの過去問・解説一覧です。">
  <title>${config.name} 過去問・解説一覧 - 岡山大学大学院入試アーカイブ</title>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/subject.css">
</head>
<body>
  <header class="header">
    <div class="container header-content">
      <a class="logo logo-link" href="../index.html">岡山大学大学院入試アーカイブ</a>
      <nav class="nav" aria-label="主要ナビゲーション">
        <ul class="nav-list">
          <li><a href="../index.html" class="nav-link">ホーム</a></li>
          <li><a href="../index.html#subjects" class="nav-link">科目一覧</a></li>
          <li><a href="../about.html" class="nav-link">サイトについて</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <nav class="breadcrumb" aria-label="パンくずリスト">
      <div class="container"><a href="../index.html">ホーム</a><span aria-hidden="true">/</span><span>${config.name}</span></div>
    </nav>
    <section class="subject-header">
      <div class="container subject-header-content">
        <div class="subject-icon-large"><img src="../images/${config.icon}" alt="" width="80" height="80"></div>
        <div class="subject-info">
          <p class="subject-kicker">2003–2024年度</p>
          <h1 class="subject-title">${config.name}</h1>
          <p class="subject-description">${config.description}</p>
        </div>
      </div>
    </section>

    <section class="exam-list" aria-labelledby="year-list-title">
      <div class="container">
        <div class="list-heading">
          <div><p class="eyebrow">22年分を収録</p><h2 class="section-title" id="year-list-title">年度を選ぶ</h2></div>
          <p>「HTML解説あり」はブラウザで解説を読めます。「年度資料」は問題PDFと収録済み資料を案内します。</p>
        </div>
        <div class="years-grid">${cards}
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <p class="footer-text">非公式・学習目的の岡山大学大学院入試アーカイブ</p>
      <p class="footer-subtext"><a href="../about.html">利用案内と免責事項</a></p>
    </div>
  </footer>
</body>
</html>
`;
}

let generatedCount = 0;
for (const subject of Object.keys(subjects)) {
  for (const year of years) {
    const examPath = path.join(root, 'exams', subject, `${year}.html`);
    const size = fs.statSync(examPath).size;
    const knownIncomplete = subject === 'math' && year === 2003;
    if (size >= 1000 && !knownIncomplete) continue;
    const questionPath = findPdf('question', subject, year);
    if (!questionPath) throw new Error(`Question PDF not found: ${subject} ${year}`);
    const answerPath = findPdf('answer', subject, year);
    fs.writeFileSync(examPath, archivePage(subject, year, questionPath, answerPath), 'utf8');
    generatedCount += 1;
  }
}

for (const subject of Object.keys(subjects)) {
  fs.writeFileSync(path.join(root, 'pages', subjects[subject].page), subjectPage(subject), 'utf8');
}

console.log(`Generated ${generatedCount} archive pages and ${Object.keys(subjects).length} subject indexes.`);
