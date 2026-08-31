"""Move the 2003--2008 hand-built explanations onto the subject page UI.

The legacy pages keep their audited prose and equations, but no longer carry a
second archive layout.  Fluid equations are converted from nested ``sub`` /
``sup`` HTML into MathJax AsciiMath before the new page is written.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


ROOT = Path(__file__).resolve().parents[1]

SUBJECTS = {
    "math": {
        "name": "数学",
        "css": "math.css",
        "icon": "fa-infinity",
        "index": "math.html",
        "years": [2003],
    },
    "fluid": {
        "name": "流体力学",
        "css": "fluid.css",
        "icon": "fa-water",
        "index": "fluid_mechanics.html",
        "years": list(range(2003, 2009)),
    },
}

ERAS = {2003: "H15", 2004: "H16", 2005: "H17", 2006: "H18", 2007: "H19", 2008: "H20"}

ASCII_REPLACEMENTS = {
    "ρ": " rho ", "μ": " mu ", "θ": " theta ", "α": " alpha ", "β": " beta ",
    "φ": " phi ", "ψ": " psi ", "Ψ": " Psi ", "γ": " gamma ", "ω": " omega ", "Ω": " Omega ", "Γ": " Gamma ",
    "ν": " nu ", "τ": " tau ", "Δ": " Delta ", "δ": " delta ", "π": " pi ",
    "∂": "partial ", "∇": "nabla ", "∫": "int ", "∞": "oo",
    "√": " sqrt ", "≤": " <= ", "≥": " >= ", "≈": " ~~ ", "≃": " ~~ ",
    "±": " +- ", "×": " xx ", "≫": " >> ", "·": " * ", "−": "-", "½": "(1/2)",
    "Ḣ": "dot(H)",
}


def formula_text(node: Tag) -> str:
    """Convert legacy inline formula markup into AsciiMath source."""

    def walk(part: Tag | NavigableString) -> str:
        if isinstance(part, NavigableString):
            return str(part)
        inner = "".join(walk(child) for child in part.children)
        if part.name == "sub":
            return f"_({inner})"
        if part.name == "sup":
            return f"^({inner})"
        if part.name == "br":
            return " "
        return inner

    value = html.unescape(walk(node))
    for source, target in ASCII_REPLACEMENTS.items():
        value = value.replace(source, target)
    value = re.sub(r"\s+", " ", value).strip()
    return value.replace("`", "")


def convert_formulas(fragment: Tag) -> None:
    for formula in list(fragment.select(".formula")):
        rendered = NavigableString(f"`{formula_text(formula)}`")
        if formula.name == "p":
            formula.clear()
            formula.append(rendered)
            formula["class"] = ["math-block"]
        else:
            formula.replace_with(rendered)


def page_assets(source: BeautifulSoup) -> tuple[str, str]:
    question = source.select_one(".resource-card--question")
    answer = source.select_one(".resource-card--answer")
    if not question or not answer:
        raise ValueError("question or answer PDF link is missing")
    return str(question.get("href")), str(answer.get("href"))


def group_questions(guide: Tag) -> list[tuple[str, list[Tag]]]:
    groups: list[tuple[str, list[Tag]]] = []
    current_title: str | None = None
    current_nodes: list[Tag] = []
    for child in guide.children:
        if not isinstance(child, Tag):
            continue
        if child.name == "h2" or "note" in child.get("class", []):
            continue
        if child.name == "h3":
            if current_title is not None:
                groups.append((current_title, current_nodes))
            current_title = child.get_text(" ", strip=True)
            current_nodes = []
        elif current_title is not None:
            current_nodes.append(child)
    if current_title is not None:
        groups.append((current_title, current_nodes))
    return groups


def node_markup(node: Tag) -> str:
    classes = set(node.get("class", []))
    inner = node.decode_contents()
    if "final-answer" in classes:
        return f'<div class="answer-highlight">{inner}</div>'
    if "math-block" in classes:
        return f'<div class="math-block">{inner}</div>'
    if node.name == "p":
        lead = node.get_text(" ", strip=True)[:40]
        if re.search(r"仮定|記号|条件監査|不足条件", lead):
            return f'<div class="example-box"><p class="problem-statement">{inner}</p></div>'
        if re.search(r"最終答|途中式・答|条件付きの答", lead):
            return f'<div class="answer-highlight">{inner}</div>'
        return f'<div class="solution-step">{inner}</div>'
    return str(node)


def make_page(subject: str, year: int, source_text: str) -> str:
    config = SUBJECTS[subject]
    source = BeautifulSoup(source_text, "html.parser")
    guide = source.select_one('.study-guide[aria-labelledby="solution-title"]')
    if guide is None:
        raise ValueError(f"{subject}/{year}: detailed explanation block is missing")
    convert_formulas(guide)
    question_href, answer_href = page_assets(source)
    groups = group_questions(guide)
    if not groups:
        raise ValueError(f"{subject}/{year}: no questions found")

    question_sections = []
    toc_items = []
    for index, (title, nodes) in enumerate(groups, start=1):
        anchor = f"question-{index}"
        toc_items.append(f'<li><a href="#{anchor}">{html.escape(title)}</a></li>')
        body = "\n".join(node_markup(node) for node in nodes)
        question_sections.append(
            f'''<section class="exam-question" aria-labelledby="{anchor}">
              <h2 class="main-section-title" id="{anchor}">{html.escape(title)}</h2>
              {body}
            </section>'''
        )

    previous = f'<a href="{year - 1}.html">← {year - 1}年度</a>' if year > 2003 else "<span></span>"
    following = f'<a href="{year + 1}.html">{year + 1}年度 →</a>' if year < 2024 else "<span></span>"
    overview = f"{len(groups)}題の条件、導出、最終結果を順に確認できます。"
    return f'''<!DOCTYPE html>
<html lang="ja" data-page-status="available">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="岡山大学大学院入試 {config['name']} {year}年度の問題と解説。">
  <title>{config['name']} {year}年度 解説 - 岡山大学大学院入試アーカイブ</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
  <link rel="stylesheet" href="../../css/{config['css']}">
  <script>
    window.MathJax = {{
      loader: {{ load: ['input/asciimath'] }},
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      asciimath: {{ delimiters: [['`', '`']] }},
      options: {{ skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }}
    }};
  </script>
  <script id="MathJax-script" defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="page-wrapper">
    <div class="header-decoration"></div>
    <header class="page-content">
      <div class="header-nav">
        <h1 class="exam-title"><i class="fas {config['icon']} mr-3 text-blue-600"></i>{year}（{ERAS[year]}）年　{config['name']}</h1>
        <div class="nav-buttons">
          <a href="../../pages/{config['index']}" class="about-link">{config['name']}一覧に戻る</a>
          <a href="../../index.html#subjects" class="about-link">トップページに戻る</a>
        </div>
      </div>
    </header>

    <div class="page-content">
      <section class="problem-overview-section" aria-labelledby="overview-title">
        <h2 id="overview-title">問題概要</h2>
        <p>{overview}</p>
        <a href="{question_href}" class="pdf-link" target="_blank" rel="noopener"><i class="fas fa-file-pdf"></i> 問題PDF</a>
        <a href="{answer_href}" class="pdf-link" target="_blank" rel="noopener"><i class="fas fa-file-pdf"></i> 解答PDF</a>
      </section>

      <hr class="separator-line">
      <div class="exam-grid exam-grid--overview">
        <main class="exam-col-left">
          {''.join(question_sections)}
        </main>
        <aside class="exam-col-right" aria-label="ページ内案内">
          <div class="point-box exam-toc">
            <div class="section-title"><i class="fas fa-list mr-2"></i>大問へ移動</div>
            <ol>{''.join(toc_items)}</ol>
          </div>
          <div class="point-box">
            <div class="section-title"><i class="fas fa-file-pdf mr-2"></i>資料</div>
            <p><a href="{question_href}" target="_blank" rel="noopener">問題PDF</a></p>
            <p><a href="{answer_href}" target="_blank" rel="noopener">解答PDF</a></p>
          </div>
        </aside>
      </div>

      <nav class="exam-year-nav" aria-label="年度間ナビゲーション">
        {previous}<a href="../../pages/{config['index']}">年度一覧</a>{following}
      </nav>
    </div>
    <footer class="site-footer">岡山大学大学院入試アーカイブ</footer>
  </div>
</body>
</html>
'''


def main() -> None:
    for subject, config in SUBJECTS.items():
        for year in config["years"]:
            target = ROOT / "exams" / subject / f"{year}.html"
            source_text = target.read_text(encoding="utf-8")
            if 'class="exam-grid exam-grid--overview"' in source_text and f'../../css/{config["css"]}' in source_text:
                print(f"{target.relative_to(ROOT)} (already migrated)")
                continue
            target.write_text(make_page(subject, year, source_text), encoding="utf-8", newline="\n")
            print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
