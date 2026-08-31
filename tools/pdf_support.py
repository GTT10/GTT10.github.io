"""Shared helpers for reproducible Japanese PDF generators."""

from __future__ import annotations

import os
from pathlib import Path


def resolve_japanese_font() -> Path:
    """Return an embeddable Japanese TrueType font or raise a useful error."""
    candidates: list[Path] = []
    configured = os.environ.get("GTT10_JAPANESE_FONT")
    if configured:
        candidates.append(Path(configured).expanduser())

    candidates.extend(
        [
            Path(r"C:\Windows\Fonts\yumin.ttf"),
            Path(r"C:\Windows\Fonts\YuGothR.ttc"),
            Path("~/.fonts/ipag.ttf").expanduser(),
            Path("/usr/share/fonts/truetype/ipafont-gothic/ipag.ttf"),
            Path("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"),
            Path("/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"),
        ]
    )

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    searched = "\n  - ".join(str(path) for path in candidates)
    raise FileNotFoundError(
        "An embeddable Japanese TrueType font was not found. "
        "Set GTT10_JAPANESE_FONT to a .ttf/.ttc file supported by ReportLab."
        f"\nSearched:\n  - {searched}"
    )
