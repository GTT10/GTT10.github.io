"""Audit the complete question/answer PDF inventory and corrected booklets."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF_ROOT = ROOT / "pdfs"
SUBJECTS = ("math", "fluid", "materials", "thermo")
YEARS = range(2003, 2025)

REQUIRED_TEXT = {
    "pdfs/answer/2003_unofficial/2003_math.pdf": (
        "100万倍", "0.69", "ベクトル関数", "周期三角波",
    ),
    "pdfs/answer/2003_unofficial/2003_fluid.pdf": (
        "糸端", "0.5 cm/s", "二次元微小検査領域", "Strouhal", "Euler",
    ),
    "pdfs/answer/2003_unofficial/thermo_2003_H15_april_answer.pdf": (
        "散逸機構", "一意に描けません", "Carnot",
    ),
    "pdfs/answer/2007_unofficial/thermo_2007_H19_april_answer.pdf": (
        "一意に定まりません", "分子量", "顕熱成分", "cv=αT",
    ),
}


def matching_pdfs(kind: str, subject: str, year: int) -> list[Path]:
    base = PDF_ROOT / kind
    matches: list[Path] = []
    for folder in base.iterdir():
        if not folder.is_dir() or not folder.name.startswith(str(year)):
            continue
        for path in folder.glob("*.pdf"):
            lower = path.name.lower()
            if subject in lower and str(year) in lower:
                matches.append(path)
    return sorted(matches)


pdf_files = sorted(PDF_ROOT.rglob("*.pdf"))
errors: list[str] = []
total_pages = 0
extracted_text: dict[Path, str] = {}

for pdf_file in pdf_files:
    relative = pdf_file.relative_to(ROOT).as_posix()
    if pdf_file.stat().st_size == 0:
        errors.append(f"{relative}: empty file")
        continue
    try:
        reader = PdfReader(pdf_file)
        pages = len(reader.pages)
        if pages == 0:
            errors.append(f"{relative}: zero pages")
        total_pages += pages
        if relative in REQUIRED_TEXT:
            extracted_text[pdf_file] = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:  # pragma: no cover - diagnostic output
        errors.append(f"{relative}: {exc}")

for kind in ("question", "answer"):
    for subject in SUBJECTS:
        for year in YEARS:
            matches = matching_pdfs(kind, subject, year)
            if len(matches) != 1:
                rendered = ", ".join(path.relative_to(ROOT).as_posix() for path in matches) or "none"
                errors.append(f"{kind} {subject} {year}: expected 1 PDF, found {len(matches)} ({rendered})")

for relative, required_phrases in REQUIRED_TEXT.items():
    path = ROOT / relative
    text = extracted_text.get(path, "")
    for phrase in required_phrases:
        if phrase not in text:
            errors.append(f"{relative}: corrected content missing {phrase!r}")

answer_hashes: dict[str, list[str]] = defaultdict(list)
for path in sorted((PDF_ROOT / "answer").rglob("*.pdf")):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    answer_hashes[digest].append(path.relative_to(ROOT).as_posix())
shared_answer_groups = [paths for paths in answer_hashes.values() if len(paths) > 1]

expected_files = len(SUBJECTS) * len(tuple(YEARS)) * 2
print(f"PDF files: {len(pdf_files)} (expected {expected_files})")
print(f"Total pages: {total_pages}")
print(f"Inventory slots: {expected_files}")
print(f"Shared answer groups: {len(shared_answer_groups)}")
for paths in shared_answer_groups:
    print("INFO shared answer source: " + ", ".join(paths))
if len(pdf_files) != expected_files:
    errors.append(f"PDF inventory: expected {expected_files} files, found {len(pdf_files)}")

print(f"Errors: {len(errors)}")
for error in errors:
    print(f"ERROR {error}")

raise SystemExit(1 if errors else 0)
