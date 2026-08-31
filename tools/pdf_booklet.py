"""Small ReportLab renderer shared by corrected answer booklets."""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab import rl_config
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from pdf_support import resolve_japanese_font


rl_config.invariant = 1
FONT_NAME = "GTT10JapaneseBooklet"
pdfmetrics.registerFont(TTFont(FONT_NAME, str(resolve_japanese_font())))

_styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "BookletTitle", parent=_styles["Title"], fontName=FONT_NAME,
    fontSize=17, leading=23, alignment=TA_CENTER, spaceAfter=4 * mm,
)
SUBTITLE = ParagraphStyle(
    "BookletSubtitle", parent=_styles["Normal"], fontName=FONT_NAME,
    fontSize=8.5, leading=12, alignment=TA_CENTER, textColor="#465365",
    spaceAfter=4 * mm,
)
H1 = ParagraphStyle(
    "BookletH1", parent=_styles["Heading1"], fontName=FONT_NAME,
    fontSize=13, leading=18, textColor="#17365d", spaceBefore=5 * mm,
    spaceAfter=2 * mm,
)
BODY = ParagraphStyle(
    "BookletBody", parent=_styles["BodyText"], fontName=FONT_NAME,
    fontSize=9.2, leading=14, alignment=TA_LEFT, wordWrap="CJK",
    spaceAfter=2 * mm,
)
FORMULA = ParagraphStyle(
    "BookletFormula", parent=BODY, fontSize=8.8, leading=13.5,
    leftIndent=5 * mm, rightIndent=3 * mm, backColor="#f3f7fb",
    borderPadding=2 * mm, spaceBefore=1 * mm, spaceAfter=2.5 * mm,
)
ANSWER = ParagraphStyle(
    "BookletAnswer", parent=BODY, leftIndent=4 * mm, rightIndent=2 * mm,
    backColor="#eef8f4", borderColor="#77b99e", borderWidth=.6,
    borderPadding=2 * mm, spaceBefore=1 * mm, spaceAfter=3 * mm,
)
NOTE = ParagraphStyle(
    "BookletNote", parent=BODY, fontSize=8.2, leading=12,
    textColor="#505c6d", leftIndent=4 * mm, rightIndent=2 * mm,
)


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text).replace("\n", "<br/>"), style)


def build_booklet(
    output: Path,
    *,
    title: str,
    subtitle: str,
    source: str,
    sections: list[dict[str, object]],
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output), pagesize=A4, leftMargin=17 * mm, rightMargin=17 * mm,
        topMargin=15 * mm, bottomMargin=17 * mm, title=title,
        author="GTT10.github.io non-official answer audit",
    )

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(FONT_NAME, 7.4)
        canvas.setFillColorRGB(.35, .39, .45)
        canvas.drawString(17 * mm, 9 * mm, "非公式解説 - 問題原本からの独立再計算")
        canvas.drawRightString(193 * mm, 9 * mm, str(document.page))
        canvas.restoreState()

    story = [
        paragraph(title, TITLE),
        paragraph(subtitle, SUBTITLE),
        paragraph(f"問題原本: {source}", NOTE),
        Spacer(1, 2 * mm),
    ]
    styles = {"body": BODY, "formula": FORMULA, "answer": ANSWER, "note": NOTE}
    for section in sections:
        story.append(paragraph(str(section["title"]), H1))
        for kind, text in section["blocks"]:
            story.append(paragraph(str(text), styles[str(kind)]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
