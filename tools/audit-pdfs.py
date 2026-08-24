from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
pdf_files = sorted((ROOT / "pdfs").rglob("*.pdf"))
total_pages = 0
errors: list[str] = []

for pdf_file in pdf_files:
    try:
        reader = PdfReader(pdf_file)
        total_pages += len(reader.pages)
    except Exception as exc:  # pragma: no cover - diagnostic output
        errors.append(f"{pdf_file.relative_to(ROOT)}: {exc}")

print(f"PDF files: {len(pdf_files)}")
print(f"Total pages: {total_pages}")
print(f"Errors: {len(errors)}")

for error in errors:
    print(f"- {error}")

raise SystemExit(1 if errors else 0)
